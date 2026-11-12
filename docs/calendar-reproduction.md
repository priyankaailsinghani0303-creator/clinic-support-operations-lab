# Missing Appointment — Calendar Filter Investigation

**Result:** Visibility issue reproduced and resolved by restoring the facility filter. No software defect established.

| Test context | Details |
|---|---|
| Platform | OpenEMR 8.5.0 public demo |
| Capture date | November 12, 2026 |
| Calendar date | November 19, 2026 |
| Sample appointment | 08:00, Stone, Alex; provider Billy Smith |
| Method | AI-assisted browser investigation using existing public-demo data |
| Changes made | Calendar date and facility view only; no appointment created, edited, or deleted |

## Support scenario

A front-desk user cannot see an appointment in the current calendar view. This is a simulated support scenario, separate from the fictional T001 ticket and its SLA timestamps.

**Potential impact:** Staff may assume the appointment is missing and create a duplicate.

## Reproduction and verification

Keep the calendar date and provider unchanged throughout the facility-filter test.

### 1. Confirm the appointment exists

Select **All Facilities**. The sample appointment appears at **08:00** under **Billy Smith**.

![Appointment visible with All Facilities selected](screenshots/01-appointment-visible.jpg)

### 2. Reproduce the visibility issue

Select **Aurora Breadth Clinic** in the facility dropdown. The appointment disappears from the current view.

![Appointment hidden with Aurora Breadth Clinic selected](screenshots/02-appointment-hidden.jpg)

### 3. Restore the view and verify

Select **All Facilities** again. The same appointment reappears at **08:00**. No replacement booking is needed.

![Appointment visible after restoring All Facilities](screenshots/03-appointment-restored.jpg)

## Expected versus actual behavior

| View | Expected | Observed |
|---|---|---|
| All Facilities | Existing appointment visible | Visible at 08:00 |
| Aurora Breadth Clinic | Appointments from other facilities excluded | Sample appointment hidden |
| All Facilities restored | Existing appointment visible again | Same appointment reappeared |

**Finding:** The observed behavior is consistent with facility filtering. This test reproduced the symptom of a missing appointment; it did not establish a software bug.

## Suggested customer reply

> Thanks for flagging this. Please confirm the appointment date and provider, then check the facility dropdown on the left. Select All Facilities to see whether the appointment appears. In this demo test, restoring that view made the appointment visible again. Please avoid creating a duplicate until the original booking has been checked.

## Escalation decision

No engineering escalation is indicated by this test. If the appointment remains missing with the correct date, provider, and facility selected, continue investigation:

- Verify whether the booking record and confirmation exist.
- Establish whether one or multiple appointments or users are affected.
- Record expected versus actual behavior and exact reproduction steps.
- Collect sanitized errors and screenshots through approved channels.
- Escalate with clinic impact, findings, an accountable owner, and the next update.

## Evidence and limitations

- Screenshots were captured through an AI-assisted browser session, not a live customer session.
- Existing public-demo sample data was used; no real clinic records were supplied.
- The calendar test was completed once; broader platform behavior was not tested.
- This does not verify Health Hue Hub functionality.
- A narrated walkthrough has not yet been recorded.

[Back to portfolio](../README.md) · [Booking troubleshooting SOP](platform-support-sop.md#8-booking--calendar-troubleshooting)
