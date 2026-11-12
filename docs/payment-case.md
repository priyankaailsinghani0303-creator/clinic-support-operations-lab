# T002 — Payment failure: written investigation and escalation exercise

> Fictional tabletop exercise. All dialogue below is drafted, not sent. No payment processor, customer account, transaction log or live demo was accessed. This demonstrates communication and investigation planning, not a successful payment fix.

## Intake and evidence boundary

| Field | Recorded information |
|---|---|
| Source | T002 in tickets.csv |
| Clinic | Demo Wellness Clinic (fictional) |
| Report | Clinic staff cannot process card payments |
| Priority / status | High / Open; impact-based priority requires confirmation |
| Historical first response | 50 minutes against a 30-minute fictional target; breached |
| Expected behavior | An authorized payment attempt returns a clear status and an auditable transaction reference |
| Actual behavior | Payment failure reported in the fictional intake; error and transaction state unknown |
| Environment / scope | Browser, terminal, processor, affected users and time window not supplied |
| Reproduction | Not attempted; no authorized payment test environment available |
| Root cause | Unknown |
| Outcome | Open; no payment success, refund or customer resolution claimed |

## Draft customer conversation

**Support:** Thanks for flagging this. I understand this is holding up checkout. Are all payment attempts affected, or one transaction? Please share the approximate time and displayed error, without card numbers or security codes. Before retrying, check whether the original attempt is pending or completed.

**Clinic — hypothetical follow-up:** We are frustrated and need to know whether we should try again.

**Support:** I understand the pressure at the front desk. I cannot yet confirm whether the first attempt charged the card. Please avoid another attempt until its status is checked through the approved payment view. I would review the transaction reference and error with our payments specialists. In this exercise, the next update is scheduled for 11:30 UTC, even if the investigation is still open.

No payment status is inferred from that hypothetical reply.

## Investigation record

| Check | Evidence currently available | Next action |
|---|---|---|
| Confirm impact and scope | Intake description only | Ask whether one or all attempts, users and terminals are affected |
| Check original transaction status | Not available | Authorized specialist to inspect processor status and transaction reference |
| Record exact error and environment | Not available | Request sanitized error and browser/terminal details |
| Compare platform and processor status | Not available | Compare authorized records before any retry |
| Reproduce safely | Not attempted | Use approved sandbox and test credentials only; never real card data |
| Verify a fix | No fix applied | Confirm transaction state and customer workflow before closure |

## Proposed specialist handoff — not submitted

- **Receiving team:** Payments Team for transaction-status investigation. A software-defect finding would instead require Engineering Team review.
- **Accountable support owner:** Proposed Demo Agent B; no assignment accepted.
- **Impact:** Checkout disruption reported; extent and workaround unknown.
- **Evidence:** Fictional intake and response timing only. No screenshots, logs or processor references available.
- **Question for specialist:** Can the original transaction state be established, and is there a discrepancy between platform and processor records?
- **Next action:** Obtain authorized status evidence before recommending a retry.
- **Update commitment:** Proposed 11:30 UTC on November 12, 2026.
- **Acceptance:** Pending; support communication ownership would remain with the support agent until accepted transfer.
- **Closure criterion:** Verified transaction outcome, safe next step communicated, and clinic confirmation documented.

[Shift handoff](shift-handoff.md) · [Back to portfolio](../README.md)
