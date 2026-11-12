# Resolution time and recurring-issue review — fictional exercise

> Separate synthetic exercise using R-series records, not T001–T003. These timestamps and outcomes are invented training fixtures, not customer outcomes or actual demo observations. This does not change active-queue status, first-response compliance or the dashboard's historical results.

## Resolution clock

For this exercise only, resolution means the synthetic workflow is restored and confirmation recorded. Elapsed UTC minutes = (resolved_at − created_at) / 60 seconds, with no business-hour pauses. Reopened tickets and paused clocks are outside scope. Compare against the reference targets in sla_policy.csv; these are not contractual commitments.

| Exercise ID | Priority | Created at (UTC) | Resolved at (UTC) | Elapsed minutes | Reference target | Exercise result |
|---|---|---|---|---:|---:|---|
| R001 | Urgent | 2026-11-12 09:00 | 2026-11-12 10:30 | 90 | 120 | Within reference target |
| R002 | High | 2026-11-12 09:00 | 2026-11-12 13:30 | 270 | 240 | Exceeds reference target by 30 minutes |
| R003 | Medium | 2026-11-12 09:00 | Not recorded | Cannot evaluate | 480 | No resolved-time calculation |

Auditable arithmetic: R001 = 1 hour 30 minutes = 90 minutes; R002 = 4 hours 30 minutes = 270 minutes. Two records are evaluable; one is within target. This 50% exercise result is separate from the active queue's 50% first-response result.

Active-queue automated resolution monitoring remains unimplemented. This written exercise demonstrates clock definitions and interpretation, not a new dashboard feature.

## Recurring-issue tabletop

The following additional reports are hypothetical inputs, not measured incidents:

| Exercise report | Fictional clinic | Report time (UTC) | Reported symptom | Verification |
|---|---|---|---|---|
| P001 | Demo Clinic North | 2026-11-12 10:05 | SMS reminder delayed | Delivery evidence unavailable |
| P002 | Demo Clinic South | 2026-11-12 10:20 | SMS reminder delayed | Delivery evidence unavailable |

**Review note at 10:25 UTC:** Two fictional clinics report a similar symptom within 15 minutes. This is a signal to investigate a shared dependency, not proof of an outage or common root cause.

**Proposed action:** Support lead to compare notification triggers, send timestamps, delivery status and provider errors through approved tools. Keep separate ticket ownership. Escalate promptly to Engineering if evidence supports a widespread technical failure; maintain customer updates while scope remains uncertain.

**Next review:** 10:40 UTC in this tabletop. If no common cause is found, continue individual investigations and record that result. No outage prevention or customer-impact reduction is claimed.

[Back to portfolio](../README.md)
