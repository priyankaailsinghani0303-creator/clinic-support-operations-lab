from pathlib import Path

import pandas as pd
import streamlit as st

from ticket_router import route_ticket

BASE_DIR = Path(__file__).resolve().parent
st.set_page_config(page_title="Clinic Support Dashboard", page_icon="🏥", layout="wide")
st.title("🏥 Clinic Support Operations Dashboard")
st.caption("Healthcare SaaS portfolio demonstration · Fictional clinic tickets, teams and SLA policies · No live integrations")


@st.cache_data
def load_tickets():
    data = pd.read_csv(BASE_DIR / "tickets.csv", dtype={"ticket_id": str})
    required = {"ticket_id", "clinic", "issue_type", "priority", "status", "description"}
    if missing := required - set(data.columns):
        raise ValueError(f"tickets.csv is missing: {sorted(missing)}")
    for col in ["clinic", "issue_type", "priority", "status"]:
        data[col] = data[col].fillna("").astype(str).str.strip().str.title()
    data["ticket_id"] = data["ticket_id"].str.strip()
    if data["ticket_id"].duplicated().any():
        raise ValueError("Duplicate ticket IDs in tickets.csv")
    return data


@st.cache_data
def load_sla_sources():
    policy = pd.read_csv(BASE_DIR / "sla_policy.csv")
    timestamps = pd.read_csv(BASE_DIR / "ticket_timestamps.csv", dtype={"ticket_id": str})
    if missing := {"priority", "first_response_minutes"} - set(policy.columns):
        raise ValueError(f"sla_policy.csv is missing: {sorted(missing)}")
    if missing := {"ticket_id", "created_at", "first_responded_at"} - set(timestamps.columns):
        raise ValueError(f"ticket_timestamps.csv is missing: {sorted(missing)}")
    policy["priority"] = policy["priority"].fillna("").astype(str).str.strip().str.title()
    timestamps["ticket_id"] = timestamps["ticket_id"].astype(str).str.strip()
    if policy["priority"].duplicated().any() or timestamps["ticket_id"].duplicated().any():
        raise ValueError("Duplicate SLA policy priorities or timestamp ticket IDs")
    return policy, timestamps


def classify_sla(row):
    target = row["first_response_minutes"]
    if pd.isna(target) or target <= 0:
        return "Policy Missing"
    if pd.isna(row["created_parsed"]):
        return "Creation Time Missing/Invalid"
    if pd.isna(row["first_responded_at"]) or str(row["first_responded_at"]).strip() == "":
        return "Response Not Recorded"
    if pd.isna(row["responded_parsed"]) or row["response_minutes"] < 0:
        return "Invalid Response Timestamp"
    return "Met" if row["response_minutes"] <= target else "Breached"


try:
    tickets = load_tickets()
    policy, timestamps = load_sla_sources()
except (FileNotFoundError, ValueError, pd.errors.EmptyDataError) as exc:
    st.error(f"Unable to load dashboard data: {exc}")
    st.stop()

if tickets.empty:
    st.warning("No tickets available.")
    st.stop()

st.sidebar.header("Support Filters")

def sidebar_filter(column, label):
    options = sorted(tickets[column].dropna().unique().tolist())
    return st.sidebar.multiselect(label, options, default=options)

clinics = sidebar_filter("clinic", "Clinic")
priorities = sidebar_filter("priority", "Priority")
statuses = sidebar_filter("status", "Status")
issue_types = sidebar_filter("issue_type", "Issue Type")

filtered = tickets[
    tickets["clinic"].isin(clinics)
    & tickets["priority"].isin(priorities)
    & tickets["status"].isin(statuses)
    & tickets["issue_type"].isin(issue_types)
].copy()

sla = filtered.merge(
    policy[["priority", "first_response_minutes"]], on="priority", how="left", validate="many_to_one"
).merge(
    timestamps[["ticket_id", "created_at", "first_responded_at"]],
    on="ticket_id", how="left", validate="one_to_one"
)
sla["first_response_minutes"] = pd.to_numeric(sla["first_response_minutes"], errors="coerce")
sla["created_parsed"] = pd.to_datetime(sla["created_at"], errors="coerce", utc=True)
sla["responded_parsed"] = pd.to_datetime(sla["first_responded_at"], errors="coerce", utc=True)
sla["response_minutes"] = (sla["responded_parsed"] - sla["created_parsed"]).dt.total_seconds() / 60
sla["SLA Status"] = sla.apply(classify_sla, axis=1)

# Shared simulation state survives Streamlit reruns and tab changes.
if "sim_ticket_id" not in st.session_state:
    st.session_state.sim_ticket_id = str(tickets.iloc[0]["ticket_id"])
if "sim_elapsed" not in st.session_state:
    st.session_state.sim_elapsed = 0


def simulation_status(elapsed, target):
    if elapsed > target:
        return "BREACHED"
    if elapsed >= 0.8 * target:
        return "AT RISK"
    return "ON TRACK"


def simulation_action(status):
    if status == "BREACHED":
        return "Escalate to the support lead, update the clinic, and document the missed target."
    if status == "AT RISK":
        return "Prioritize the ticket, verify ownership, and send a first response before the deadline."
    return "Continue monitoring the queue and respond within the target."

# Only simulate tickets that have a valid SLA target in the complete dataset.
all_targets = tickets[["ticket_id", "issue_type", "priority"]].merge(
    policy[["priority", "first_response_minutes"]], on="priority", how="left", validate="many_to_one"
)
all_targets["first_response_minutes"] = pd.to_numeric(all_targets["first_response_minutes"], errors="coerce")
valid_targets = all_targets[all_targets["first_response_minutes"] > 0].copy()
valid_ids = valid_targets["ticket_id"].tolist()
if valid_ids and st.session_state.sim_ticket_id not in valid_ids:
    st.session_state.sim_ticket_id = valid_ids[0]

sim_row = None
sim_target = None
sim_status = None
if valid_ids:
    sim_row = valid_targets.loc[valid_targets["ticket_id"] == st.session_state.sim_ticket_id].iloc[0]
    sim_target = float(sim_row["first_response_minutes"])
    sim_status = simulation_status(st.session_state.sim_elapsed, sim_target)

st.subheader("Support Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tickets", len(filtered))
c2.metric("Urgent Tickets", int(filtered["priority"].eq("Urgent").sum()))
c3.metric("Open Tickets", int(filtered["status"].eq("Open").sum()))
c4.metric("High Priority", int(filtered["priority"].isin(["High", "Urgent"]).sum()))

overview_tab, queue_tab, sla_tab, routing_tab, risk_tab = st.tabs(
    ["Overview", "Ticket Queue", "SLA Monitoring", "Ticket Routing", "SLA Risk Alerts"]
)

with overview_tab:
    st.subheader("Connected SLA Risk Simulation")
    st.caption("Simulation only. Changing the slider does not modify ticket records or historical SLA compliance.")
    if sim_row is None:
        st.info("No ticket with a valid SLA policy is available for simulation.")
    else:
        st.write(f"**Simulated ticket:** {st.session_state.sim_ticket_id} · {sim_row['issue_type']} · {sim_row['priority']}")
        x, y, z = st.columns(3)
        x.metric("Simulated Risk", sim_status)
        y.metric("Simulated Elapsed", f"{st.session_state.sim_elapsed} min")
        z.metric("Simulated SLA Target", f"{sim_target:g} min")
        st.info(f"Recommended action: {simulation_action(sim_status)}")
        st.caption("Adjust the elapsed-time slider in the SLA Risk Alerts tab. The status here updates when Streamlit reruns.")

    st.subheader("Historical SLA Summary")
    met = int(sla["SLA Status"].eq("Met").sum())
    breached = int(sla["SLA Status"].eq("Breached").sum())
    recorded = met + breached
    h1, h2, h3 = st.columns(3)
    h1.metric("Historical SLA Met", met)
    h2.metric("Historical SLA Breached", breached)
    h3.metric("Historical Compliance", f"{met / recorded:.1%}" if recorded else "N/A")
    st.caption("Compliance denominator includes only valid, recorded first responses.")

    st.subheader("Ticket Analytics")
    if filtered.empty:
        st.info("No tickets match the current filters.")
    else:
        left, right = st.columns(2)
        with left:
            st.write("Tickets by Priority")
            st.bar_chart(filtered["priority"].value_counts())
            st.write("Tickets by Clinic")
            st.bar_chart(filtered["clinic"].value_counts())
        with right:
            st.write("Tickets by Status")
            st.bar_chart(filtered["status"].value_counts())
            st.write("Tickets by Issue Type")
            st.bar_chart(filtered["issue_type"].value_counts())

with queue_tab:
    st.subheader("Support Ticket Queue")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("Download Filtered Tickets", filtered.to_csv(index=False),
                       "clinic_support_tickets.csv", "text/csv")

with sla_tab:
    st.subheader("Historical First-Response SLA Monitoring")
    st.caption("Recorded response outcomes from fictional ticket timestamps. Not a live countdown.")
    met = int(sla["SLA Status"].eq("Met").sum())
    breached = int(sla["SLA Status"].eq("Breached").sum())
    missing = int(sla["SLA Status"].eq("Response Not Recorded").sum())
    evaluated = met + breached
    a, b, c = st.columns(3)
    a.metric("SLA Met", met)
    b.metric("SLA Breached", breached)
    c.metric("Response Not Recorded", missing)
    st.metric("First-Response SLA Compliance", f"{met / evaluated:.1%}" if evaluated else "N/A")
    st.subheader("Ticket SLA Details")
    st.dataframe(sla[["ticket_id", "clinic", "issue_type", "priority",
                      "first_response_minutes", "response_minutes", "SLA Status"]],
                 use_container_width=True, hide_index=True)
    if not sla.empty:
        st.subheader("SLA Status Distribution")
        st.bar_chart(sla["SLA Status"].value_counts())
    st.subheader("Support Escalation Alerts")
    if breached:
        st.error(f"{breached} ticket(s) breached the historical first-response SLA. Review and escalate.")
    if missing:
        st.warning(f"{missing} ticket(s) have no recorded first response. Verify response history.")
    for label in ["Creation Time Missing/Invalid", "Invalid Response Timestamp", "Policy Missing"]:
        count = int(sla["SLA Status"].eq(label).sum())
        if count:
            st.warning(f"{count} ticket(s): {label}. Review the source data.")
    if not sla.empty and sla["SLA Status"].eq("Met").all():
        st.success("All selected tickets with records met their first-response targets.")
    st.download_button("Download SLA Report", sla.to_csv(index=False), "clinic_sla_report.csv", "text/csv")

with routing_tab:
    st.subheader("Automated Ticket Routing")
    st.caption("Rule-based demonstration assignments; not actual clinic or vendor team structures.")
    if filtered.empty:
        st.info("No tickets match the current filters.")
    else:
        routed = pd.DataFrame([route_ticket(row) for row in filtered.to_dict(orient="records")])
        r1, r2, r3 = st.columns(3)
        r1.metric("Tickets Routed", len(routed))
        r2.metric("Support Teams", routed["assigned_team"].nunique())
        r3.metric("Urgent Tickets", int(routed["priority"].eq("Urgent").sum()))
        st.subheader("Ticket Assignment Queue")
        st.dataframe(routed, use_container_width=True, hide_index=True)
        st.subheader("Tickets by Assigned Team")
        st.bar_chart(routed["assigned_team"].value_counts())
        st.subheader("Routing Decisions")
        for _, item in routed.iterrows():
            st.info(f"{item['ticket_id']} · {item['issue_type']} → {item['assigned_team']}")
        st.download_button("Download Routing Report", routed.to_csv(index=False),
                           "clinic_ticket_routing.csv", "text/csv")

with risk_tab:
    st.subheader("Proactive SLA Risk Alerts — Simulation")
    st.caption("Hypothetical unanswered ticket. This is a rule-based demonstration, not live monitoring or ML prediction.")
    if not valid_ids:
        st.info("No valid SLA policies are available for simulation.")
    else:
        st.selectbox("Select a support ticket", options=valid_ids, key="sim_ticket_id")
        selected = valid_targets.loc[valid_targets["ticket_id"] == st.session_state.sim_ticket_id].iloc[0]
        target = float(selected["first_response_minutes"])
        slider_max = max(int(target * 2), 30, int(st.session_state.sim_elapsed))
        st.write(f"**Issue:** {selected['issue_type']} · **Priority:** {selected['priority']} · **SLA target:** {target:g} minutes")
        st.slider("Simulated minutes since ticket creation (no first response yet)",
                  min_value=0, max_value=slider_max, step=1, key="sim_elapsed")
        elapsed = st.session_state.sim_elapsed
        status = simulation_status(elapsed, target)
        remaining = target - elapsed
        st.progress(min(elapsed / target, 1.0))
        m1, m2, m3 = st.columns(3)
        m1.metric("Elapsed Time", f"{elapsed} min")
        m2.metric("SLA Target", f"{target:g} min")
        m3.metric("Time Remaining", f"{max(remaining, 0):g} min")
        if status == "BREACHED":
            st.error("BREACHED — Simulated elapsed time exceeds the response deadline.")
        elif status == "AT RISK":
            st.warning("AT RISK — At least 80% of the simulated response window has elapsed.")
        else:
            st.success("ON TRACK — Below the simulated warning threshold.")
        st.subheader("Recommended Support Action")
        st.info(simulation_action(status))
        st.subheader("Simulation Result")
        result = pd.DataFrame([{
            "ticket_id": st.session_state.sim_ticket_id,
            "priority": selected["priority"],
            "sla_target_minutes": target,
            "simulated_elapsed_minutes": elapsed,
            "remaining_minutes": remaining,
            "risk_status": status,
            "recommended_action": simulation_action(status),
        }])
        st.dataframe(result, use_container_width=True, hide_index=True)
        st.download_button("Download Risk Simulation", result.to_csv(index=False),
                           "clinic_sla_risk_simulation.csv", "text/csv")

st.divider()
st.caption("Clinic Support Operations Lab · Fictional portfolio demonstration · No live healthcare data, live SLA monitoring, or AI predictions")
