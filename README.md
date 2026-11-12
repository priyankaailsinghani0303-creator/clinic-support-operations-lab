# Clinic Support Operations Lab

**A clinic support workspace for ticket triage, SLA review, and team handoffs.**

Explore how booking, payment, and messaging issues move through a healthcare SaaS support workflow—from an incoming clinic request to a prioritized action and team assignment.

Built with **Python · Streamlit · pandas · CSV · Markdown**

> Portfolio demonstration using fictional clinics and tickets. The dashboard runs locally; this repository does not currently link to a hosted demo.

## Start Here

| Explore | What you will find |
| --- | --- |
| [Sample support queue](tickets.csv) | Three clinic scenarios covering booking, payments, and messaging |
| [SLA results](#sample-sla-results) | Response targets, recorded response times, and recommended follow-up |
| [Interactive dashboard](dashboard.py) | Five views for reviewing the queue, SLA performance, routing, and simulated risk |
| [Customer help article](docs/help-article.md) | A step-by-step missing-appointment guide for clinic staff |
| [Support operations SOP](docs/platform-support-sop.md) | Triage, troubleshooting, communication, escalation, and shift handoffs |
| [Run locally](#run-locally) | Dashboard setup and command-line reports |

## The Support Problem

Clinic staff need a clear next step when a booking is missing, a payment cannot be processed, or a reminder is not delivered. Support teams need to see which requests are urgent, which response targets were missed, and who should own the next action.

This lab brings those decisions into one small, inspectable workflow:

1. Review the clinic request and its assigned priority.
2. Compare recorded first-response time with the configured SLA.
3. Identify breaches and incomplete records for follow-up.
4. Suggest a support team using issue-based routing rules.
5. Use documented troubleshooting and handoff procedures to guide the next step.

## Dashboard Features

| View | Capabilities | Support decision |
| --- | --- | --- |
| **Overview** | Ticket counts, priority and issue charts, historical SLA metrics | Understand the current sample workload |
| **Ticket Queue** | Filter by clinic, priority, status, and issue type; export CSV | Focus on the requests that need review |
| **SLA Monitoring** | Compare first responses with targets; surface breaches and data-quality flags; export results | Identify missed response targets and records to verify |
| **Ticket Routing** | Suggest teams using fixed issue-type rules; export assignments | Clarify the proposed handoff owner |
| **SLA Risk Alerts** | Adjust hypothetical elapsed time and view a recommended action | Explore when an unanswered ticket would approach or exceed its target |

The risk simulator is separate from historical reporting. It uses a slider, not a live clock: **on track** below 80% of the response window, **at risk** from 80% through the deadline, and **breached** after the deadline.

## Sample SLA Results

These expected results come from the committed fictional data, not measured customer outcomes.

| Ticket | Clinic issue | Priority | First response | Target | Result |
| --- | --- | --- | --- | --- | --- |
| T001 | Booking missing from calendar | Urgent | 10 min | 15 min | Met |
| T002 | Unable to process card payments | High | 50 min | 30 min | Breached |
| T003 | Appointment reminders not delivered | Medium | No timestamp record | 120 min | Requires record verification |

**Sample first-response compliance: 50% — 1 of 2 evaluated tickets met its target.**

T003 has no row in the timestamp file and is excluded from that percentage. The command-line checker labels it `RESPONSE NOT RECORDED`; the dashboard labels it `Creation Time Missing/Invalid` because its creation time is also unavailable.

| Ticket | Recommended next action |
| --- | --- |
| T001 | Continue follow-up on the unresolved booking issue; meeting a response target does not mean the issue is resolved |
| T002 | Review the breach, update the clinic, and notify the support lead |
| T003 | Verify creation and response history before determining SLA status |

### Demonstration SLA Policy

| Priority | First-response target |
| --- | --- |
| Urgent | 15 minutes |
| High | 30 minutes |
| Medium | 120 minutes |
| Low | 240 minutes |

Targets are configurable in [sla_policy.csv](sla_policy.csv). Calculations use elapsed minutes rather than business hours. The policy file also contains resolution targets; this lab evaluates **first-response compliance**, not resolution compliance.

### Routing Rules

| Issue type | Suggested team |
| --- | --- |
| Booking | Platform Support |
| Payments | Billing Support |
| Messaging | Technical Support |
| Account | Account Support |
| Unrecognized type | General Support |

Assignments are illustrative recommendations. They do not create tickets or notify external teams.

## Customer Support Documentation

### Missing Appointment Help Article

[Read the customer-facing guide →](docs/help-article.md)

A troubleshooting article for nontechnical clinic staff, covering date and calendar checks, provider selection, booking status, and escalation information. It is generic portfolio guidance rather than verified instructions for a specific vendor.

### Platform Support SOP

[Read the support operations procedure →](docs/platform-support-sop.md)

A reference covering intake and prioritization, booking/payment/messaging troubleshooting, customer communication, bug-report requirements, engineering escalation, screen-share support, SLA review, and end-of-shift handoffs.

The SOP describes a proposed process. It is not evidence that a vendor defect was reproduced or a real customer incident was resolved.

## Run Locally

Use **Python 3.10 or later**. Run the following commands from a terminal.

### 1. Clone and install

```bash
git clone https://github.com/priyankaailsinghani0303-creator/clinic-support-operations-lab.git
cd clinic-support-operations-lab
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead of the `source` command.

### 2. Launch the dashboard

```bash
python3 -m streamlit run dashboard.py
```

Open the local URL printed in the terminal.

### 3. Explore the workflow

1. Open **Ticket Queue** and filter by priority.
2. Review T002 in **SLA Monitoring** against its 30-minute target.
3. Open **Ticket Routing** to inspect the suggested teams.
4. In **SLA Risk Alerts**, select T001 and move the slider to 12, 15, and 16 minutes to compare warning and breach behavior.
5. Download a CSV report for review or handoff.

### Optional: Command-line reports

```bash
python3 sla_checker.py
python3 ticket_router.py
```

These two scripts use the Python standard library and do not require Streamlit or pandas.

## Repository Guide

| File | Purpose |
| --- | --- |
| [dashboard.py](dashboard.py) | Interactive Streamlit workspace |
| [sla_checker.py](sla_checker.py) | Command-line SLA evaluation, triage queue, and follow-up recommendations |
| [ticket_router.py](ticket_router.py) | Command-line team routing |
| [tickets.csv](tickets.csv) | Fictional clinic requests, priorities, and statuses |
| [ticket_timestamps.csv](ticket_timestamps.csv) | Recorded creation and first-response times |
| [sla_policy.csv](sla_policy.csv) | Demonstration response and resolution targets |
| [requirements.txt](requirements.txt) | Dashboard dependencies |
| [docs/help-article.md](docs/help-article.md) | Customer-facing troubleshooting guide |
| [docs/platform-support-sop.md](docs/platform-support-sop.md) | Support workflow reference |

## Skills Demonstrated

- **Support operations:** priority-based triage, response-target review, and escalation recommendations.
- **Workflow automation:** CSV processing and rule-based team assignment.
- **Reporting:** filterable tables, charts, sample metrics, and downloadable reports.
- **Customer communication:** clear troubleshooting instructions for clinic staff.
- **Process documentation:** proposed bug-report requirements, escalation procedures, and handoff standards.

## Scope and Limitations

- All clinic requests and SLA targets are fictional. No real patient data is included.
- The three-ticket dataset demonstrates behavior; it does not establish performance at scale.
- The application reads repository CSV files. It does not persist ticket edits, send messages, or connect to an EHR, payment processor, or helpdesk.
- Risk alerts are hypothetical rule-based outputs, not live monitoring or AI predictions.
- Authentication, access controls, and production deployment hardening are outside the current implementation.
- This is a portfolio prototype, not a production support system or a claim of regulatory compliance.
