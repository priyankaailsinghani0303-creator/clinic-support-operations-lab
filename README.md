# Clinic Support Operations Lab

Support operations portfolio for a healthcare SaaS platform: booking, calendar, payments, messaging, and account settings—for busy clinic staff who need clear, practical help.

**My approach:** Understand the issue, guide initial troubleshooting, keep the clinic informed, and escalate with useful context.

### [Open Live Dashboard →](https://clinic-support-operations-lab-qzcgaprlcsp8dvyn7ql4rb.streamlit.app/)

## What’s Inside

| Work Sample | Skill Demonstrated |
| :--- | :--- |
| **[Interactive Dashboard](https://clinic-support-operations-lab-qzcgaprlcsp8dvyn7ql4rb.streamlit.app/)** | Ticket organization, first-response SLA monitoring, team routing, and risk simulation |
| **[Customer Help Article](docs/help-article.md)** — Missing Appointment | Clear troubleshooting guidance for nontechnical front-desk staff |
| **[Support SOP](docs/platform-support-sop.md)** — Triage → Troubleshoot → Update → Escalate | Structured investigations, customer communication, and handoff procedures |

## Three Fictional Clinic Scenarios

### T001 — Booking Missing From Calendar · Urgent

The clinic cannot locate an appointment. The help article guides staff through date, calendar-filter, provider, and booking-status checks.

> First response: **10 min / 15 min target — Met**
>
> Next action: Continue troubleshooting and confirm the appointment’s status. Meeting the response target does not mean the issue is resolved.

### T002 — Card Payments Failing · High

The clinic reports being unable to process payments. The SOP outlines transaction-status checks, information collection, customer updates, and escalation criteria.

> First response: **50 min / 30 min target — Breached**
>
> Recommended action: Flag the breach, update the clinic, and escalate with investigation details.

### T003 — Appointment Reminders Not Delivered · Medium

The clinic reports missing reminders. The SOP covers notification triggers, delivery status, and whether multiple recipients are affected.

> **Timestamp records missing — verify history before determining SLA status.**

## Bug-Report Structure

The SOP documents how to capture:

- Expected versus actual behavior.
- Environment and steps to reproduce.
- Reproduction outcome and clinic impact.
- Sanitized screenshots, timestamps, or error messages when available.
- Troubleshooting already attempted.
- Next action and receiving team.

## Explore the Dashboard

1. **Overview:** Review ticket counts, priorities, and sample SLA performance.
2. **Ticket Queue:** Filter requests by clinic, priority, status, and issue type.
3. **SLA Monitoring:** Review response-target breaches and incomplete records.
4. **Ticket Routing:** Inspect suggested support-team assignments.
5. **SLA Risk Alerts:** Adjust hypothetical elapsed time to explore warning and breach thresholds.

Downloadable CSV reports support further review and handoffs.

## Run Locally

Requires **Python 3.10 or later**. Download or clone this repository, open its folder in a terminal, and run:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run dashboard.py
```

**Tools:** Python · Streamlit · pandas · CSV · Markdown

---

*Independent portfolio demonstration using fictional clinics, tickets, and SLA targets. No real patient information is included. SLA reporting evaluates first responses using elapsed time; risk alerts are hypothetical simulations. Bug reproduction and screen sharing are documented procedures, not completed demonstrations. Not affiliated with Health Hue Digital.*


## Canonical Rules and Ownership

Numeric targets come from `sla_policy.csv`. The dashboard, SLA checker and ticket router share `support_rules.py`. Issue type selects an initial team; reviewed priority selects the SLA tier. Booking, Payments and Messaging start with Platform Support; Account starts with Account Support; Other or unknown input goes to General Support triage.

Routing is a suggestion. `assigned_owner` is blank in these fictional records because no named owner has accepted assignment. Operational tickets require one accountable owner; specialist escalation retains that owner until an accepted transfer is recorded.

Historical results: T001 Met, T002 Breached, T003 Creation Time Missing/Invalid. Two evaluable tickets yield 50% compliance; one ticket cannot be evaluated. Missing history is not a confirmed breach. Resolution targets are reference values, not measured performance.

`tickets_backup.csv` is an inactive historical snapshot. No script loads it; `tickets.csv` is the active queue. Do not restore the snapshot as current policy or assignment data.

Leadership decisions and detailed status definitions are documented in the [support SOP](docs/platform-support-sop.md). Run `python -m unittest discover -s tests -v` to verify shared rules.
