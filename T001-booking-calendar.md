# T001 — Booking Not Appearing in Clinic Calendar

**Ticket ID:** T001
**Clinic:** Demo Aesthetic Clinic
**Issue Type:** Booking
**Priority:** Urgent
**Status:** Open

> Fictional support scenario for portfolio demonstration. Not a verified software defect.

## Issue Description

Clinic staff report that an appointment booked through the online booking page does not appear in their clinic calendar.

## Expected Behavior

When a patient successfully books an appointment online, the appointment should appear in the clinic calendar with the correct date, time, and provider.

## Reported Behavior

The clinic reports that the appointment is missing from the calendar.

 **Verification status:** Hands-on booking test completed in OpenEMR on November 12, 2026. The appointment appeared correctly in the provider calendar. The original fictional missing-booking issue was not reproduced; its root cause remains unknown.

## Troubleshooting Checklist

- [ ] Confirm the appointment was successfully submitted.
- [ ] Check the selected appointment date and time.
- [ ] Verify the correct provider and calendar are selected.
- [ ] Check whether calendar filters are hiding the appointment.
- [ ] Verify the appointment status (confirmed, pending, or cancelled).
- [ ] Check whether the issue occurs after refreshing the calendar.
- [ ] Attempt to reproduce the issue using fictional test data.

**Investigation status:** Initial hands-on investigation completed using the OpenEMR public demo. Appointment creation and calendar visibility were successfully tested. The original reported issue was not reproduced, and its root cause remains undetermined.

## Proposed Steps to Reproduce

1. Open a fictional clinic booking system using a test account.
2. Select an available appointment service.
3. Choose a provider, date, and time.
4. Submit the appointment booking.
5. Open the clinic calendar.
6. Navigate to the selected appointment date.
7. Check whether the new appointment appears.

## Expected Result

The appointment appears in the correct provider's calendar at the selected date and time.

## Actual Result

Not yet tested. The clinic-reported issue is that the appointment does not appear.

## Reproduction Status

Not attempted. Requires a working test booking application.

## Engineering Escalation Checklist

- [ ] Record the affected feature and clinic account.
- [ ] Record the date and time of the reported issue.
- [ ] Identify the affected provider and appointment.
- [ ] Record the browser and device used.
- [ ] Document troubleshooting steps already completed.
- [ ] Record whether the issue can be reproduced.
- [ ] Attach sanitized screenshots or error messages if available.
- [ ] Describe the impact on clinic operations.

## Escalation Decision

**Status:** Pending investigation.

Escalate to engineering if a suspected product defect is supported by reproducible evidence or if the issue cannot be resolved through standard troubleshooting.

**Privacy:** Do not include real patient names, medical records, payment details, or other sensitive information in this public portfolio.
## Hands-On Investigation — OpenEMR Demo

**Test date:** November 12, 2026  
**Application:** OpenEMR 8.5.0 Public Demo  
**Test environment:** Chrome browser on Chromebook  
**Scenario:** T001 — Booking Not Appearing in Clinic Calendar  
**Test type:** Manual functional investigation  
**Defect status:** Not reproduced

### Test Objective

Determine whether an appointment created through the OpenEMR scheduling interface appears in the correct provider calendar.

### Test Steps and Observations

| Step | Action | Observed Result |
|---|---|---|
| 1 | Opened OpenEMR Calendar | Calendar loaded successfully |
| 2 | Opened the appointment form | Appointment configuration fields displayed |
| 3 | Selected an existing demo patient | Patient selection completed |
| 4 | Selected provider Billy Smith | Provider displayed in appointment form |
| 5 | Searched for available appointments over 7 days | No openings displayed |
| 6 | Extended availability search to 30 days | Available appointment times displayed |
| 7 | Selected November 12, 2026, at 10:00 AM | Appointment form updated to 10:00 |
| 8 | Saved the appointment | Appointment form closed |
| 9 | Checked the provider calendar | Appointment appeared at 10:00 AM |

### Expected Result

The saved appointment should appear on the correct provider calendar at the selected date and time.

### Actual Result

The appointment appeared on Billy Smith's calendar on November 12, 2026, at 10:00 AM.

**Outcome: PASS — Booking and calendar visibility worked in this test.**

### Additional Observation

The initial seven-day availability search displayed no openings, while a subsequent 30-day search displayed available times, including times on the original start date.

The cause of this difference was not determined. Further controlled testing would be necessary before classifying it as a software defect.

### Investigation Conclusion

The original fictional complaint of a missing appointment was not reproduced in this OpenEMR test.

The investigation demonstrated appointment creation, availability searching, provider selection and calendar verification.

No engineering escalation is warranted based solely on this successful booking test.

### Evidence

- [T001 Booking Verification Screenshot](T001-booking-verified.png.png)

*This investigation was conducted in a public OpenEMR demo environment using demo data. It does not represent testing of Health Hue Hub itself.*
