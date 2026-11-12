# Clinic Support Operations Lab

A lightweight Python portfolio project demonstrating healthcare SaaS customer support workflows.

## Project Overview

This project simulates support operations for fictional clinics, including appointment booking, payment processing, and patient messaging issues.

## SLA Monitoring — Sample Report

This project uses fictional clinic support tickets to demonstrate
first-response SLA monitoring and escalation prioritization.

| Ticket | Issue | Priority | Response Time | SLA Target | Result |
|---|---|---|---|---|---|
| T001 | Booking / Calendar | Urgent | 10 min | 15 min | MET |
| T002 | Payments | High | 50 min | 30 min | BREACHED |
| T003 | Messaging | Medium | Not recorded | 120 min | RESPONSE NOT RECORDED |

### Performance Summary

- Total tickets: 3
- Tickets with recorded responses: 2
- SLA met: 1
- SLA breached: 1
- Missing response records: 1
- First-response SLA compliance: 50%

### Recommended Support Actions

- T001: Continue normal follow-up.
- T002: Review SLA breach, update clinic, notify support lead.
- T003: Verify response history and contact clinic if needed.

**Note:** These are expected results based on the
committed fictional CSV data. The script calculates
response times and identifies tickets requiring attention.

[View Python SLA Checker](sla_checker.py)


## Customer Support Documentation

### Customer Help Article
[How to Find a Missing Appointment in Your Clinic Calendar](docs/help-article.md)

A customer-facing troubleshooting guide written for nontechnical clinic staff, demonstrating clear communication, step-by-step guidance, and patient privacy awareness.

### Platform Support SOP
[View Platform Support Standard Operating Procedure](docs/platform-support-sop.md)

Documents ticket triage, troubleshooting workflows, customer communication, engineering escalation, and support handoffs.


## Skills Demonstrated

- Support ticket triage and prioritization
- First-response SLA monitoring
- SLA breach detection
- Missing-response identification
- Support queue reporting
- Escalation recommendations
- Structured bug reporting and troubleshooting

## Technology

- Python 3
- CSV files
- Markdown documentation

## Run the Project

```bash
python3 sla_checker.py
```

## Bug Report

## Data and Limitations

All clinics, tickets, and SLA targets are fictional. This is a command-line simulation, not a deployed helpdesk platform.

SLA calculations use elapsed time. Missing responses are tracked separately from confirmed breaches.
