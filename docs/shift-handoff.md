# Three-ticket shift handoff — fictional exercise

> Written as of November 12, 2026, 11:00 UTC. Proposed names, actions and deadlines below are training examples, not accepted assignments or sent promises. The active CSV intentionally retains blank assigned_owner fields. All three tickets remain Open.

| Ticket | Current evidence / status | Proposed support owner | Next action | Proposed next update (UTC) |
|---|---|---|---|---|
| T001 · Urgent | Fictional calendar issue; first response 10/15 minutes, Met. Separate OpenEMR investigation does not establish resolution of T001 | Demo Agent A | Confirm actual clinic impact, booking status, date/provider/facility filters; avoid duplicate booking | November 12, 2026, 11:15 |
| T002 · High | Fictional payment failure; first response 50/30 minutes, Breached. Transaction state unknown | Demo Agent B | Check authorized transaction evidence; seek Payments review; notify lead of response breach | November 12, 2026, 11:30 |
| T003 · Medium | Fictional reminder failure; no timestamp row, so response SLA cannot be evaluated | Demo Agent C | Recover source history; clarify SMS/email scope and expected send time; request authorized delivery evidence | November 12, 2026, 12:00 |

## Receiving-shift actions

1. Support lead confirms one accountable owner per ticket before accepting this handoff.
2. Receiving agent records acceptance time and customer-update commitment in the operational system.
3. Prioritize confirmed impact; the sample priorities alone do not establish an outage.
4. Do not infer that T003 is unanswered or breached from absent history.
5. Review promised updates even when there is no new technical finding.

**Accepted by / acceptance time:** Not accepted — tabletop example only.

**Proposed specialist escalation:** T002 Payments Team review, pending evidence and acceptance. No engineering escalation or software defect has been established.

**Shift counts:** Three open tickets; one recorded response breach; one unevaluable first-response record; no documented resolutions.

[Payment case](payment-case.md) · [Back to portfolio](../README.md)
