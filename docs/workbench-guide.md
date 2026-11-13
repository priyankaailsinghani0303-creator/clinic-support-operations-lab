# Interactive support workbench

This is an independently runnable portfolio application with original synthetic fixtures. It does not depend on a public OpenEMR demo, real clinic accounts or paid integrations. It is AI-assisted work, not evidence of unaided candidate performance.

## Run on a Chromebook with Codespaces

1. Open this repository in GitHub Codespaces (Code → Codespaces → create a codespace). Availability depends on your GitHub quota.
2. In its terminal run `pip install -r requirements.txt`.
3. Run `streamlit run workbench.py` and open the forwarded port 8501.
4. Create a fictional case. Use a fictional agent name and write your own response.

For Streamlit Community Cloud, create a separate app with `workbench.py` as its entry point. The existing `dashboard.py` remains a historical reporting demonstration. No hosted deployment is claimed by this change.

## Reviewer walkthrough

For each scenario: create a ticket → accept ownership and set an update deadline → record a response → perform both evidence checks → apply the simulator action → verify → record a clearly labelled role-play customer confirmation → resolve with a summary → download the report.

| Scenario | Simulator finding | Verification |
|---|---|---|
| Calendar | Existing booking belongs to a facility excluded by the current view | Original booking visible; count remains one |
| Payments | Processor succeeded but platform status lags | Refresh reconciles statuses; attempt count remains one |
| Messaging | Reminder suppressed before provider send because consent is absent | Separate, consented synthetic recipient passes a new reminder test; original preferences unchanged |

These findings are designed fixtures, not discoveries about Health Hue or external software. The simulator returns predefined results only after its prerequisites are met. It is a workflow practice tool, not a replica of a processor or clinical platform.

## What is implemented

- SQLite-backed records and timestamped event history within a session.
- Accepted support ownership, update deadlines and recorded responses.
- Evidence prerequisites and verified-closure gates.
- Historical and active response/resolution clocks using elapsed UTC minutes.
- Reopening with original creation clock, preserved prior events and reset verification.
- Escalation recording while retaining the support owner; no specialist acceptance mechanism.
- Queue CSV and investigation/shift-handoff Markdown exports.
- Repeated open-symptom counts for manual review, without claiming outage detection.

## Persistence and deployment boundaries

Each browser session receives a separate temporary SQLite database. Reruns retain its records, but session resets and host restarts can lose them. The core can reopen a database path in a local workflow; the public UI deliberately does not share a database between reviewers. Export before leaving. Temporary directories are subject to host cleanup and are not a backup.

This is a functional portfolio MVP. It is not production healthcare software: authentication, role-based authorization, durable managed storage, retention/cleanup jobs, monitoring, migrations, encrypted backups, external integrations and deployment hardening have not been implemented or assessed. Do not enter real patient data. Event records are application history, not a tamper-proof compliance audit log.

## Independent candidate demonstration

Record yourself operating the workbench and explaining why you choose each check. Use your own words. Explain that fixtures and outcomes are synthetic and the implementation was AI-assisted. Do not describe simulator completion as real customer resolution or rewrite the historical T001–T003 cases as solved.

The original OpenEMR case still needs an independent restoration capture if you want to claim that external verification. This workbench does not supply that evidence.
