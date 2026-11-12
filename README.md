# Clinic Support Operations Lab

A healthcare SaaS support portfolio showing how I approach booking, calendar, payment, messaging, and account-access issues for busy clinic teams.

I am a medical student with approximately two years of hospital administration experience, including appointments, patient calls, complaints, billing queries, and hospital software. This project applies that experience to platform support.

**My approach:** Understand the impact, explain the next step clearly, investigate systematically, and keep ownership through escalation.

### [Open the Live Dashboard →](https://clinic-support-operations-lab-qzcgaprlcsp8dvyn7ql4rb.streamlit.app/)

No local installation required to review the dashboard.

> Independent portfolio project using fictional clinics, tickets, and SLA targets. No real patient information is included. Not affiliated with Health Hue Digital.

## Start Here

| Work Sample | What to Look For |
|---|---|
| **[Live Support Dashboard](https://clinic-support-operations-lab-qzcgaprlcsp8dvyn7ql4rb.streamlit.app/)** | Ticket filtering, first-response SLA results, incomplete records, suggested routing, and simulated risk alerts |
| **[Customer Help Article: Missing Appointment](docs/help-article.md)** | Simple troubleshooting steps for nontechnical clinic staff, with clear guidance on when to contact support |
| **[Platform Support SOP](docs/platform-support-sop.md)** | Triage, troubleshooting, customer updates, bug-report requirements, escalation, screen-sharing procedures, and shift handoffs |

## Three Clinic Support Scenarios

The sample queue contains three open tickets. Priorities are fictional assumptions that would require confirmation of actual clinic impact.

| Ticket | Reported Issue | Investigation Focus | Sample First-Response Result |
|---|---|---|---|
| **T001 · Urgent** | Online appointments missing from the calendar | Confirm booking status, date, provider, and calendar filters before creating another appointment | **Met:** 10 minutes against a 15-minute target |
| **T002 · High** | Clinic staff cannot process card payments | Check transaction status, error details, and scope; distinguish payment discrepancies from suspected software defects | **Breached:** 50 minutes against a 30-minute target |
| **T003 · Medium** | Appointment reminders not delivered | Identify SMS/email scope, expected send time, notification triggers, and delivery status | **Cannot evaluate:** timestamp history is missing |

**How to interpret the results:** Two tickets can be evaluated; one met its first-response target. The sample compliance rate is **50% across those two tickets**. T003 is excluded because its history is incomplete.

Meeting a response target does not mean the issue has been resolved.

## My Support Workflow

| Step | Skill Demonstrated | Supporting SOP Sections |
|---|---|---|
| **1. Receive & Triage** | Acknowledge the request, clarify impact, and assign priority | [§6 Customer Communication](docs/platform-support-sop.md#6-customer-communication-standards) · [§7 Ticket Triage](docs/platform-support-sop.md#7-support-ticket-triage-flowchart) |
| **2. Troubleshoot** | Guide focused checks and document findings | [§8 Booking & Calendar](docs/platform-support-sop.md#8-booking--calendar-troubleshooting) · [§9 Payments](docs/platform-support-sop.md#9-payment--pos-troubleshooting) · [§10 Messaging](docs/platform-support-sop.md#10-messaging--notification-troubleshooting) · [§11 Account Access](docs/platform-support-sop.md#11-account-access--settings-troubleshooting) |
| **3. Investigate & Escalate** | Document reproduction attempts, evidence, and a clear escalation | [§12 Bug Reproduction & Documentation](docs/platform-support-sop.md#12-bug-reproduction--technical-documentation) · [§15 Specialist Escalation](docs/platform-support-sop.md#15-specialist-escalation-matrix) · [§3 Ownership](docs/platform-support-sop.md#3-roles-and-responsibilities) |
| **4. Guide & Educate** | Explain features clearly and help clinic staff repeat the steps independently | [§13 Screen Sharing & Training](docs/platform-support-sop.md#13-screen-share-support--customer-training) · [§16 Help Article Management](docs/platform-support-sop.md#16-knowledge-base--help-article-management) |
| **5. Track & Review** | Monitor response targets, incomplete records, follow-ups, and recurring issues | [§14 Ticket Documentation & SLA Management](docs/platform-support-sop.md#14-support-ticket-documentation--sla-management) · [§16.4 Continuous Improvement](docs/platform-support-sop.md#164-continuous-improvement) |
| **6. Hand Over** | Record ticket status, ownership, next actions, and outstanding customer updates | [§17.1 End-of-Shift Handoff](docs/platform-support-sop.md#171-end-of-shift-handoff) · [§17.2 Handoff Template](docs/platform-support-sop.md#172-end-of-shift-handoff-template) |

[Read the complete Platform Support SOP →](docs/platform-support-sop.md)

## Customer Communication Example

**Illustrative first reply for T001 — not a sent customer message:**

> Thanks for flagging this. I understand a missing appointment can disrupt the front desk. Could you confirm the appointment date, selected provider, and whether you received a booking confirmation? First, please check that the calendar shows the correct date and provider. Avoid creating another booking until we confirm whether the original exists. Please leave patient details out of your reply.

The aim is to acknowledge the disruption, ask focused questions, and give a practical first step.

## Escalation and Ownership

The SOP defines what an engineering handoff should contain:

- Clinic impact and affected workflow
- Expected versus actual behavior
- Environment and steps to reproduce
- Whether reproduction succeeded
- Sanitized error messages, screenshots, or timestamps when available
- Troubleshooting already attempted
- Receiving team, accountable owner, and next action

Routing suggestions do not count as accepted assignments. The support owner continues customer communication until a receiving owner accepts the handoff.

## Explore the Dashboard

| View | What It Shows |
|---|---|
| **Overview** | Sample ticket counts, priorities, and first-response SLA performance |
| **Ticket Queue** | Filters for clinic, priority, status, and issue type |
| **SLA Monitoring** | Confirmed response-target breaches and records that cannot be evaluated |
| **Ticket Routing** | Suggested initial support-team assignments |
| **SLA Risk Alerts** | Hypothetical elapsed-time scenarios showing warning and breach thresholds |

Downloadable CSV reports support further review and handoffs.

## Scope of This Demonstration

| Implemented or Written | Documented Procedure / Future Evidence |
|---|---|
| Interactive dashboard and fictional ticket queue | Completed bug reproduction with captured evidence |
| First-response SLA calculations and missing-data handling | Measured resolution times |
| Suggested initial team routing | Accepted assignments and completed handoffs |
| Customer-facing help article | Recorded screen-share walkthrough |
| Support SOP with example customer replies | Real ticket, chat, or call outcomes |

The help article provides generic troubleshooting guidance. Platform-specific instructions have not been verified against Health Hue Hub.

The SOP includes privacy-conscious practices such as requesting only necessary information, sanitizing evidence, and avoiding passwords or full payment-card details.

## Technical Notes

**Tools:** Python · Streamlit · pandas · CSV · Markdown

- SLA targets are defined in [`sla_policy.csv`](sla_policy.csv).
- The dashboard, SLA checker, and ticket router use [`support_rules.py`](support_rules.py).
- First-response calculations use elapsed time in UTC, without business-hour pauses.
- Risk alerts are hypothetical simulations.
- Resolution targets are reference values; resolution performance is not calculated.
- [`tickets.csv`](tickets.csv) is the active sample queue.
- `tickets_backup.csv` is an inactive historical snapshot.

<details>
<summary>Run locally and verify shared rules</summary>

Requires **Python 3.10 or later**.

Download or clone this repository, open its folder in a terminal, and run:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run dashboard.py
```

Run the shared-rule checks:

```bash
python3 -m unittest discover -s tests -v
```

</details>
