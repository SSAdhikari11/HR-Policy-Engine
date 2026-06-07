import frappe
from frappe.utils import get_datetime, time_diff

def time_diff_in_minutes(later, earlier):
    """Custom helper since frappe.utils removed it in v15"""
    return time_diff(later, earlier).total_seconds() / 60


def set_late_minutes(doc, method):
    """
    Calculate late minutes based on shift start time & check-in.
    Only if Late Entry Marking is enabled in Shift Type.
    Considers grace period before marking late.
    """
    if not doc.shift or not doc.in_time:
        return

    shift = frappe.get_doc("Shift Type", doc.shift)

    if not shift.enable_late_entry_marking:
        return

    shift_start = get_datetime(
        doc.attendance_date.strftime("%Y-%m-%d") + " " + str(shift.start_time)
    )
    checkin_time = get_datetime(str(doc.in_time))

    late_mins = time_diff_in_minutes(checkin_time, shift_start)

    # apply grace period
    if shift.late_entry_grace_period:
        late_mins -= shift.late_entry_grace_period

    # only set positive values
    doc.custom_late_minutes = max(0, int(late_mins))
