# Clinic Support Operations Lab

Support operations portfolio for a healthcare SaaS platform: booking, calendar, payments, messaging, and account settings—for busy clinic staff who need clear, practical help.

**My approach:** Understand the issue, guide initial troubleshooting, keep the clinic informed, and escalate with useful context.

## What’s Inside

| Work Sample | Skill Demonstrated |
| :--- | :--- |
| **[Customer Help Article](docs/help-article.md)** — Missing Appointment | Clear troubleshooting guidance for nontechnical front-desk staff |
| **[Support SOP](docs/platform-support-sop.md)** — Triage → Troubleshoot → Update → Escalate | Structured investigations, customer communication, and handoff procedures |
| **[Dashboard Code](dashboard.py)** — Queue, SLAs, Routing | First-response tracking, breach identification, and suggested team ownership |

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

## Dashboard Features

- Filter tickets by clinic, priority, status, and issue type.
- Compare recorded first-response times against configurable SLA targets.
- Flag response breaches and incomplete timestamp records.
- Suggest support teams using issue-based routing rules.
- Simulate approaching response deadlines with an elapsed-time slider.
- Download ticket, SLA, routing, and simulation reports as CSV files.

## Run Locally

Requires **Python 3.10 or later**. Download or clone this repository, open its folder in a terminal, and run:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal.

**Tools:** Python · Streamlit · pandas · CSV · Markdown

---

*Independent portfolio demonstration using fictional clinics, tickets, and SLA targets. No real patient information is included. SLA reporting evaluates first responses using elapsed time; risk alerts are hypothetical simulations. Bug reproduction and screen sharing are documented procedures, not completed demonstrations. Not affiliated with Health Hue Digital.*
