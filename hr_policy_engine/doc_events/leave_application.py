import frappe
from frappe.utils import flt, getdate, add_days
from frappe.utils import get_first_day, get_last_day
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on

def apply_sandwich_rule(leave_app, method=None):
    """
    Hook: Runs when Leave Application is submitted.
    Evaluates Sandwich Leave Rules dynamically based on Leave Rule DocType config.
    Creates either Leave Deduction Log or Payroll Deduction Log based on the rule.
    """

    # Fetch active sandwich rules
    rules = frappe.get_all(
        "HR Policy Engine",
        filters={"enable": 1, "rule_type": "Sandwich", "docstatus": 1},
        fields="*"
    )
    if not rules:
        return

    from_date = getdate(leave_app.from_date)
    to_date = getdate(leave_app.to_date)
    employee = leave_app.employee
    month_key = from_date.strftime("%Y-%m")

    # Fetch all holidays (including weekends)
    all_holidays = get_all_holidays(employee)
    leave_days = (to_date - from_date).days + 1

    # Separate weekends from other holidays
    weekend_holidays = {d for d in all_holidays if d.weekday() in (5, 6)}
    public_holidays = all_holidays - weekend_holidays

    for rule in rules:
        extra_days = set()

        # --- Case 1: Weekend bridging (Sat/Sun) ---
        if rule.include_weekend:
            prev_day = add_days(from_date, -1)
            while prev_day in weekend_holidays:
                extra_days.add(prev_day)
                prev_day = add_days(prev_day, -1)

            next_day = add_days(to_date, 1)
            while next_day in weekend_holidays:
                extra_days.add(next_day)
                next_day = add_days(next_day, 1)

        # --- Case 2: Between two public holidays ---
        if rule.include_between_offs:
            prev_day = add_days(from_date, -1)
            next_day = add_days(to_date, 1)
            if prev_day in public_holidays and next_day in public_holidays:
                extra_days.add(prev_day)
                extra_days.add(next_day)

        extra_deduction_days = len(extra_days)
        total_span = leave_days + extra_deduction_days

        if total_span < 3 or extra_deduction_days <= 0:
            continue

        deduction_unit = flt(rule.deduction_unit or 1)

        # ----------------------------
        # PATH 1: Affect Leave Balance
        # ----------------------------
        if rule.affect_leave_balance:
            # Load leave priorities from child table
            priorities = frappe.db.sql(
                """
                SELECT leave_type, priority
                FROM `tabLeave Priority`
                WHERE parent = %s
                AND parenttype = 'Leave Rule'
                ORDER BY COALESCE(priority, 9999)
                """,
                (rule.name,),
                as_dict=True
            )

            if not priorities:
                frappe.log_error(f"No leave priority found for Sandwich Rule {rule.name}", "Leave Rule Warning")

            actual_deduction_unit= extra_deduction_days* deduction_unit
            remaining_deduction = actual_deduction_unit

            for row in priorities:
                leave_type = row.leave_type
                if not leave_type or remaining_deduction <= 0:
                    continue

                leave_balance = get_leave_balance_on(employee, leave_type, from_date)
                if leave_balance <= 0:
                    continue  # no balance here, move to next

                # Deduct as much as possible from this leave type
                deduction_now = min(leave_balance, remaining_deduction)

                leave_deduction_log = frappe.get_doc({
                    "doctype": "Leave Deduction Log",
                    "employee": employee,
                    "leave_type": leave_type,
                    "rule_name": rule.name,
                    "month": month_key,
                    "deduction_unit": deduction_now,
                    "reference_doctype": "Leave Application",
                    "reference_name": leave_app.name,
                })
                leave_deduction_log.insert(ignore_permissions=True)
                leave_deduction_log.submit()

                remaining_deduction -= deduction_now

            # If after all leave types, something is still left → use LWP
            if remaining_deduction > 0:
                lwp_log = frappe.get_doc({
                    "doctype": "Leave Deduction Log",
                    "employee": employee,
                    "leave_type": "Leave Without Pay",
                    "rule_name": rule.name,
                    "month": month_key,
                    "deduction_unit": remaining_deduction,
                    "reference_doctype": "Leave Application",
                    "reference_name": leave_app.name,
                })
                lwp_log.insert(ignore_permissions=True)
                lwp_log.submit()

        # ----------------------------
        # PATH 2: Payroll Direct Deduction
        # ----------------------------
        if rule.affect_payroll_directly:
            log = frappe.get_doc({
                "doctype": "Payroll Deduction Log",
                "employee": employee,
                "rule_name": rule.name,
                "month": month_key,
                "deduction_days": total_span,
                "deduction_unit": deduction_unit,
                "reference_doctype": "Leave Application",
                "reference_name": leave_app.name,
            })
            log.insert(ignore_permissions=True)
            log.submit()

def get_all_holidays(employee):
    """Fetch holiday dates for employee’s holiday list."""
    holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")
    if not holiday_list:
        return set()

    holidays = frappe.get_all(
        "Holiday",
        filters={"parent": holiday_list},
        pluck="holiday_date"
    )
    return {getdate(h) for h in holidays}