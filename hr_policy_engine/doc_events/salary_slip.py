from frappe.utils import getdate, flt, cstr
import frappe

def apply_attendance_policy_deductions(salary_slip, method):
    """
    Apply 'Attendance Policy Deduction' to Salary Slip:
    - Computes based on Attendance Deduction Log for the month
    - Updates existing row (no duplicates) or removes it if amount is 0
    - Recalculates totals and year-to-date properly
    """
    # 1) month key
    try:
        start_date = getdate(salary_slip.start_date)
        month_key = start_date.strftime("%Y-%m")
    except Exception:
        month_key = None

    # 2) fetch logs
    filters = {"employee": salary_slip.employee, "payroll_processed": 0, "docstatus":1}
    if month_key:
        filters["month"] = month_key

    if salary_slip.start_date and salary_slip.end_date:
        filters["creation"] = ["between", [salary_slip.start_date, salary_slip.end_date]]

    logs = frappe.get_all(
        "Payroll Deduction Log",
        filters=filters,
        fields=["name", "deduction_days", "deduction_unit"],
    )

    if not logs:
        return 
    
    if method=="on_submit":
        # mark logs as processed
        for l in logs:
            frappe.db.set_value("Payroll Deduction Log", l.name, "payroll_processed", 1)
        return

    # 3) compute total days
    total_days = 0.0
    for l in logs:
        days = flt(l.get("deduction_days") or 0.0)
        unit = flt(l.get("deduction_unit") or 1)  # default full day if empty
        total_days += days * unit

    if total_days == 0:
        return  # nothing to deduct

    # 4) compute deduction amount
    gross = flt(salary_slip.gross_pay)
    twd = flt(salary_slip.total_working_days)
    deduction_amount = flt((gross / twd) * total_days, 2) if gross > 0 and twd > 0 else 0.0

    # 5) locate existing deduction row
    existing = next(
        (d for d in (salary_slip.get("deductions") or [])
         if cstr(d.salary_component or "").strip() == "Attendance Policy Deduction"),
        None
    )

    # 6) apply / update / remove
    if deduction_amount > 0:
        if existing:
            existing.amount = deduction_amount
        else:
            salary_slip.append("deductions", {
                "salary_component": "Attendance Policy Deduction",
                "amount": deduction_amount,
            })
    else:
        if existing:
            salary_slip.get("deductions").remove(existing)
