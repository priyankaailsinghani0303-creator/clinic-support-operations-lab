
 Platform Support Standard Operating Procedure

**Document:** 01 — Platform Support SOP  
**Organization:** Fictional healthcare SaaS support environment  
**Prepared by:** Portfolio demonstration  
**Version:** 1.0  
**Effective date:** November 2026  
**Document status:** Demonstration 

> **Disclaimer:** This SOP is an independently developed portfolio project.

---

## 1. Purpose

This Standard Operating Procedure defines how a Platform Support Specialist handles customer support requests from medical spas and aesthetic clinics using a healthcare SaaS platform.

The goal is to provide timely, accurate, and professional support by:

- Understanding clinic staff problems quickly.
- Troubleshooting common platform issues.
- Resolving issues at first contact whenever possible.
- Documenting investigations and actions taken.
- Reproducing suspected software defects.
- Escalating unresolved technical issues with sufficient evidence.
- Keeping customers informed throughout the resolution process.
- Monitoring response times, resolution times, and recurring issues.

## 2. Scope

This SOP covers the following support activities:

- Inbound customer support tickets.
- Live chat and telephone support.
- Appointment booking and calendar troubleshooting.
- Patient record access and account settings.
- Payment and point-of-sale troubleshooting.
- Email and SMS messaging issues.
- Customer guidance through screen sharing.
- Bug reproduction and engineering escalation.
- Help article creation and maintenance.
- SLA monitoring and support reporting.

This procedure is designed for fictional training scenarios. Actual platform configurations, contractual SLAs, privacy obligations and escalation contacts must be verified before operational use.

---

## 3. Roles and Responsibilities

| Role | Responsibilities |
|---|---|
| Platform Support Specialist | Receives tickets, responds to customers, troubleshoots platform issues, documents investigations and follows up on unresolved requests. |
| Support Team Lead | Oversees ticket prioritization, monitors SLA performance, reviews escalations and supports complex customer issues. |
| Engineering Team | Investigates reproducible software defects, reviews technical evidence and works on product fixes. |
| Billing / Payments Team | Investigates payment processing issues, transaction discrepancies and billing-related escalations. |
| Clinic Owner / Administrator | Provides account information, confirms clinic configurations and coordinates access for authorized staff. |
| Clinic Front-Desk Staff | Reports booking, calendar, messaging and account issues and follows troubleshooting guidance. |

### 3.1 Support Ownership

The Platform Support Specialist remains responsible for communicating with the customer until the issue is resolved or formally handed over according to the support team's escalation process.

### 3.2 Escalation Ownership

Escalating a ticket does not mean abandoning customer communication. The assigned support specialist must document the handoff, communicate relevant updates and monitor the ticket until ownership is clearly transferred.

---

## 4. Support Coverage Hours

| Coverage Item | Requirement |
|---|---|
| Support availability | North American business hours, according to the assigned shift |
| Time zone | Shift schedule communicated in the team's designated time zone |
| Support channels | Email, live chat and telephone |
| Shift preparation | Log in before the scheduled shift and review open tickets and pending escalations |
| During shift | Monitor incoming requests, update ticket statuses and follow up on unresolved issues |
| Break coverage | Follow the team's handoff and coverage arrangements |
| End of shift | Update outstanding tickets and provide a handoff to the next assigned support specialist |
| After-hours requests | Follow the organization's documented after-hours escalation process |

**Coverage principle:** Customer requests must be acknowledged and routed according to the team's actual support schedule and agreed service-level targets.

---

---

## 5. Workstation & Pre-Shift Checklist

Before starting each shift, the Platform Support Specialist confirms:

- [ ] Quiet and private workspace suitable for customer calls.
- [ ] Headset, microphone and internet connection tested.
- [ ] Computer locked when stepping away.
- [ ] Authorized access to Health Hue Hub support environment confirmed.
- [ ] Support ticket queue opened and reviewed.
- [ ] Email and live chat channels checked.
- [ ] Internal support and escalation communication channels opened.
- [ ] SLA dashboard or tracking sheet opened.
- [ ] Troubleshooting guides and knowledge-base articles accessible.
- [ ] Pending customer follow-ups and escalations reviewed.
- [ ] No unresolved critical handoffs from the previous shift.

**Readiness standard:** The specialist should be prepared to receive, investigate, document and respond to incoming customer requests before beginning the assigned support shift.

---

---

## 6. Customer Communication Standards

| Standard | Requirement |
|---|---|
| First response | Acknowledge incoming requests within the applicable SLA target. |
| Greeting | "Thank you for contacting Health Hue Support. This is [Name]. How can I help you today?" |
| Tone | Friendly, professional, calm and solution-oriented. |
| Language | Clear, simple English without unnecessary technical jargon. |
| Understanding | Allow the customer to explain the issue without interruption. |
| Clarification | Ask focused questions to understand the problem and its impact. |
| Response quality | Provide accurate troubleshooting instructions in manageable steps. |
| Hold etiquette | Ask permission before placing a caller on hold and provide regular updates. |
| Transfer etiquette | Explain why the issue requires another team and provide relevant context before transferring. |
| Follow-up | Keep customers informed when an issue requires further investigation. |
| Sign-off | Summarize the action taken, confirm next steps and thank the customer. |

### 6.1 Communication Channels

| Channel | Standard |
|---|---|
| Email | Use clear subject lines, structured explanations and actionable next steps. |
| Live chat | Respond concisely, ask one diagnostic question at a time and guide customers step by step. |
| Telephone | Listen actively, clarify the problem and explain troubleshooting verbally. |
| Screen sharing | Obtain customer agreement, explain each action and avoid accessing unrelated sensitive information. |

---

---

## 7. Support Ticket Triage Flowchart

When a customer contacts support, the specialist identifies the issue category, evaluates its impact and follows the appropriate troubleshooting or escalation pathway.

```text
                 INCOMING SUPPORT REQUEST
                            |
                   Acknowledge customer
                            |
                   Identify issue type
                            |
       +--------------------+--------------------+
       |          |         |         |           |
     BOOKING   PAYMENTS  MESSAGING  ACCOUNT      OTHER
       |          |         |       ACCESS        |
       v          v         v         v           v
    Check      Check     Check     Check       Gather
    booking    payment   delivery  login and   details
    status     status    status    permissions
       |          |         |         |           |
       +----------+---------+---------+-----------+
                            |
                   Can support resolve it?
                       /          \
                     YES           NO
                      |             |
                 Apply fix     Document findings
                      |             |
                 Test result   Reproduce issue
                      |             |
                 Update ticket Escalate to relevant
                      |        technical team
                      |             |
                      +------+------+
                             |
                    Inform customer
                             |
                    Confirm next steps
                             |
                      Close or monitor
                         ticket
```

### 7.1 Initial Triage Requirements

The specialist records the following before beginning troubleshooting:

- Customer and clinic account identification.
- Affected platform feature.
- Description of the reported issue.
- Date and approximate time the issue occurred.
- Number of users or workflows affected.
- Error messages or screenshots, where available and safely collected.
- Business impact on clinic operations.
- Troubleshooting steps already attempted.

**Triage principle:** Prioritize issues according to customer impact, operational disruption and applicable SLA requirements. Do not assume that every technical issue is a software defect.
```


## 8. Booking & Calendar Troubleshooting

**Goal:** Identify and resolve appointment booking and calendar synchronization issues while minimizing disruption to clinic operations.

### 8.1 Common Booking Issues

| Issue | Initial Support Check |
|---|---|
| Appointment not appearing | Verify booking status, selected date and provider calendar. |
| Duplicate appointments | Check for multiple booking records before making changes. |
| Incorrect appointment time | Verify clinic time zone, selected slot and calendar settings. |
| Provider unavailable | Check provider availability and scheduling configuration. |
| Online booking failure | Review the reported error, booking steps and affected service. |
| Calendar not updating | Refresh the calendar and verify whether the booking record exists. |

### 8.2 Troubleshooting Procedure

1. Acknowledge the customer's issue and confirm the affected clinic account.
2. Ask for the appointment date, approximate booking time and affected provider.
3. Confirm whether the booking was successfully submitted.
4. Check the appointment status (confirmed, pending or cancelled).
5. Verify the selected service, provider and calendar.
6. Check whether calendar filters or date settings are hiding the appointment.
7. Ask the customer to refresh the calendar if appropriate.
8. Determine whether the issue affects one appointment or multiple bookings.
9. Document findings and actions in the support ticket.
10. Escalate suspected platform defects when the issue remains unresolved.

### 8.3 Customer Communication

**Example response:**

"Thank you for reporting this. I'll help you investigate why the appointment isn't appearing in your clinic calendar. Could you confirm the appointment date, selected provider and approximate booking time? We'll check the booking status and calendar settings first."

### 8.4 Escalation Criteria

Escalate to the appropriate technical team when:

- A successfully submitted appointment cannot be located.
- Multiple appointments are missing from the calendar.
- Calendar synchronization repeatedly fails.
- Duplicate bookings appear without an identifiable cause.
- The issue persists after standard troubleshooting.
- A reproducible software defect is suspected.

**Important:** Do not create duplicate appointments, cancel existing bookings or modify patient records without verifying the current booking status and obtaining appropriate authorization.

---
