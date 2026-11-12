# Clinic Support Operations Lab

**Healthcare SaaS support portfolio: booking, payments, messaging, and clear clinic communication.**

A small support operations demo showing how I organize clinic requests, review first-response SLAs, suggest team handoffs, and explain troubleshooting steps to nontechnical staff.

## Start Here

| Work sample | What it demonstrates |
| --- | --- |
| [Customer help article](docs/help-article.md) | Clear, step-by-step guidance for a missing appointment |
| [Support SOP](docs/platform-support-sop.md) | Triage, troubleshooting, customer updates, bug-report requirements, and escalation |
| [Dashboard source](dashboard.py) | Filterable ticket queue, SLA reporting, team routing, and an interactive risk simulation |

## Three Clinic Scenarios

| Ticket | Issue | Priority | Sample first-response result |
| --- | --- | --- | --- |
| T001 | Booking missing from calendar | Urgent | 10 min / 15 min target — met |
| T002 | Card payments failing | High | 50 min / 30 min target — breached |
| T003 | Appointment reminders not delivered | Medium | Timestamps missing — verify records |

**Next actions:** continue booking follow-up, flag the payment response breach, and verify the messaging ticket's history.

[View sample tickets](tickets.csv) · [SLA checker](sla_checker.py) · [Routing script](ticket_router.py)

## Run the Dashboard

Requires Python 3.10+. From the downloaded or cloned repository:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run dashboard.py
```

**Built with:** Python, Streamlit, pandas, CSV, and Markdown.

*Independent portfolio demonstration using fictional data—not Health Hue Hub software or verified vendor instructions. SLA calculations cover first responses using elapsed time; risk alerts are hypothetical. No real patient data is included.*
