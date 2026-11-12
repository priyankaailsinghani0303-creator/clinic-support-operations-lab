
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Clinic Support Operations Lab",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

st.title("🏥 Clinic Support Operations Lab")
st.caption(
    "Healthcare SaaS support portfolio | Fictional clinic scenarios "
    "| Rule-based workflow demonstration"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_csv(filename):
    path = BASE_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


tickets = load_csv("tickets.csv")
timestamps = load_csv("ticket_timestamps.csv")
policies = load_csv("sla_policy.csv")

required_ticket_columns = [
    "ticket_id",
    "clinic",
    "issue_type",
    "priority",
    "status",
    "description"
]

if tickets.empty:
    st.error("tickets.csv is missing or empty.")
    st.stop()

missing_columns = [
    col for col in required_ticket_columns
    if col not in tickets.columns
]

if missing_columns:
    st.error(
        "Missing ticket columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

tickets["ticket_id"] = tickets["ticket_id"].astype(str)

for col in ["clinic", "issue_type", "priority", "status"]:
    tickets[col] = tickets[col].fillna("Unknown").astype(str).str.strip()

for col in ["issue_type", "priority", "status"]:
    tickets[col] = tickets[col].str.title()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Ticket Filters")

selected_clinics = st.sidebar.multiselect(
    "Clinic",
    sorted(tickets["clinic"].unique()),
    default=sorted(tickets["clinic"].unique())
)

selected_priorities = st.sidebar.multiselect(
    "Priority",
    sorted(tickets["priority"].unique()),
    default=sorted(tickets["priority"].unique())
)

selected_statuses = st.sidebar.multiselect(
    "Status",
    sorted(tickets["status"].unique()),
    default=sorted(tickets["status"].unique())
)

selected_types = st.sidebar.multiselect(
    "Issue Type",
    sorted(tickets["issue_type"].unique()),
    default=sorted(tickets["issue_type"].unique())
)

filtered = tickets[
    tickets["clinic"].isin(selected_clinics)
    & tickets["priority"].isin(selected_priorities)
    & tickets["status"].isin(selected_statuses)
    & tickets["issue_type"].isin(selected_types)
].copy()


# --------------------------------------------------
# SLA CALCULATIONS
# --------------------------------------------------

def calculate_sla(ticket_data, timestamp_data, policy_data):
    result = ticket_data.copy()

    result["first_response_minutes"] = pd.NA
    result["response_minutes"] = float("nan")
    result["SLA Status"] = "Policy Missing"

    if not policy_data.empty and {
        "priority",
        "first_response_minutes"
    }.issubset(policy_data.columns):

        policy_data = policy_data.copy()
        policy_data["priority"] = (
            policy_data["priority"].astype(str).str.strip().str.title()
        )
        policy_data["first_response_minutes"] = pd.to_numeric(
            policy_data["first_response_minutes"],
            errors="coerce"
        )

        result = result.drop(
            columns=["first_response_minutes"]
        ).merge(
            policy_data[
                ["priority", "first_response_minutes"]
            ].drop_duplicates("priority"),
            on="priority",
            how="left"
        )

    if not timestamp_data.empty and {
        "ticket_id",
        "created_at",
        "first_responded_at"
    }.issubset(timestamp_data.columns):

        timestamp_data = timestamp_data.copy()
        timestamp_data["ticket_id"] = (
            timestamp_data["ticket_id"].astype(str)
        )

        result = result.merge(
            timestamp_data[
                ["ticket_id", "created_at", "first_responded_at"]
            ].drop_duplicates("ticket_id"),
            on="ticket_id",
            how="left"
        )

        created = pd.to_datetime(
            result["created_at"],
            errors="coerce",
            utc=True
        )

        responded = pd.to_datetime(
            result["first_responded_at"],
            errors="coerce",
            utc=True
        )

        result["response_minutes"] = (
            responded - created
        ).dt.total_seconds() / 60

        result["SLA Status"] = "Policy Missing"

        valid_policy = (
            pd.to_numeric(
                result["first_response_minutes"],
                errors="coerce"
            ) > 0
        )

        result.loc[
            valid_policy, "SLA Status"
        ] = "Creation Time Missing/Invalid"

        valid_created = created.notna() & valid_policy

        result.loc[
            valid_created, "SLA Status"
        ] = "Response Not Recorded"

        invalid_response = (
            valid_created
            & responded.notna()
            & (result["response_minutes"] < 0)
        )

        result.loc[
            invalid_response, "SLA Status"
        ] = "Invalid Response Timestamp"

        valid_response = (
            valid_created
            & responded.notna()
            & (result["response_minutes"] >= 0)
        )

        met = (
            valid_response
            & (
                result["response_minutes"]
                <= result["first_response_minutes"]
            )
        )

        breached = (
            valid_response
            & (
                result["response_minutes"]
                > result["first_response_minutes"]
            )
        )

        result.loc[met, "SLA Status"] = "Met"
        result.loc[breached, "SLA Status"] = "Breached"

    return result


sla = calculate_sla(filtered, timestamps, policies)


# --------------------------------------------------
# TICKET ROUTING
# --------------------------------------------------

ROUTING_RULES = {
    "Booking": "Platform Support",
    "Payments": "Billing Support",
    "Messaging": "Technical Support",
    "Account": "Account Support"
}


def route_ticket(ticket):
    issue_type = str(ticket.get("issue_type", "Unknown")).title()

    return {
        "ticket_id": ticket.get("ticket_id", ""),
        "issue_type": issue_type,
        "priority": ticket.get("priority", ""),
        "assigned_team": ROUTING_RULES.get(
            issue_type,
            "General Support"
        )
    }


# --------------------------------------------------
# SLA RISK SIMULATION
# --------------------------------------------------

def simulation_status(elapsed, target):
    if target <= 0:
        return "UNAVAILABLE"

    if elapsed > target:
        return "BREACHED"

    if elapsed >= target * 0.8:
        return "AT RISK"

    return "ON TRACK"


def simulation_action(status):
    if status == "BREACHED":
        return (
            "Escalate immediately, notify the support lead, "
            "and document the missed response target."
        )

    if status == "AT RISK":
        return (
            "Prioritize the ticket, notify the assigned team, "
            "and prepare escalation."
        )

    if status == "ON TRACK":
        return (
            "Continue monitoring and respond within "
            "the SLA target."
        )

    return "Verify the SLA policy."


valid_targets = sla.copy()

valid_targets["first_response_minutes"] = pd.to_numeric(
    valid_targets["first_response_minutes"],
    errors="coerce"
)

valid_targets = valid_targets[
    valid_targets["first_response_minutes"] > 0
].copy()

valid_ids = valid_targets["ticket_id"].tolist()

if valid_ids:
    if st.session_state.get("sim_ticket_id") not in valid_ids:
        st.session_state["sim_ticket_id"] = valid_ids[0]
        st.session_state["sim_elapsed"] = 0

    if "sim_elapsed" not in st.session_state:
        st.session_state["sim_elapsed"] = 0


# --------------------------------------------------
# DEFINE ALL FIVE TABS FIRST
# --------------------------------------------------

overview_tab, queue_tab, sla_tab, routing_tab, risk_tab = st.tabs(
    [
        "Overview",
        "Ticket Queue",
        "SLA Monitoring",
        "Ticket Routing",
        "SLA Risk Alerts"
    ]
)


# --------------------------------------------------
# TAB 1 — OVERVIEW
# --------------------------------------------------

with overview_tab:
    st.header("Support Operations Overview")

    total = len(filtered)
    urgent = int(filtered["priority"].eq("Urgent").sum())
    open_tickets = int(filtered["status"].eq("Open").sum())
    high = int(filtered["priority"].eq("High").sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", total)
    c2.metric("Urgent Tickets", urgent)
    c3.metric("Open Tickets", open_tickets)
    c4.metric("High Priority", high)

    st.divider()

    if filtered.empty:
        st.info("No tickets match the current filters.")
    else:
        left, right = st.columns(2)

        with left:
            st.subheader("Tickets by Priority")
            st.bar_chart(
                filtered["priority"].value_counts()
            )

        with right:
            st.subheader("Tickets by Issue Type")
            st.bar_chart(
                filtered["issue_type"].value_counts()
            )

    st.divider()

    st.subheader("Historical SLA Performance")

    met_count = int(sla["SLA Status"].eq("Met").sum())
    breach_count = int(sla["SLA Status"].eq("Breached").sum())
    missing_count = int(
        sla["SLA Status"].eq("Response Not Recorded").sum()
    )

    evaluated = met_count + breach_count

    compliance = (
        f"{met_count / evaluated:.1%}"
        if evaluated > 0
        else "N/A"
    )

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("SLA Met", met_count)
    s2.metric("SLA Breached", breach_count)
    s3.metric("Response Not Recorded", missing_count)
    s4.metric("SLA Compliance", compliance)

    st.caption(
        "Historical metrics use recorded fictional timestamps. "
        "Missing responses are excluded from compliance percentage."
    )

    st.divider()

    st.subheader("Current SLA Risk Simulation")

    if valid_ids:
        selected_id = st.session_state["sim_ticket_id"]

        selected_row = valid_targets[
            valid_targets["ticket_id"] == selected_id
        ].iloc[0]

        target = float(
            selected_row["first_response_minutes"]
        )

        elapsed = st.session_state["sim_elapsed"]

        status = simulation_status(elapsed, target)

        a, b, c = st.columns(3)

        a.metric("Simulated Ticket", selected_id)
        b.metric("Elapsed Minutes", elapsed)
        c.metric("Risk Status", status)

        if status == "BREACHED":
            st.error(
                "Simulated SLA breached. Immediate escalation recommended."
            )

        elif status == "AT RISK":
            st.warning(
                "Simulated ticket is approaching its SLA deadline."
            )

        else:
            st.success(
                "Simulated ticket is currently on track."
            )

        st.info(simulation_action(status))

        st.caption(
            "Change the slider in SLA Risk Alerts to update "
            "this Overview indicator. This is not live monitoring."
        )

    else:
        st.info(
            "No valid SLA policy is available for simulation."
        )


# --------------------------------------------------
# TAB 2 — TICKET QUEUE
# --------------------------------------------------

with queue_tab:
    st.header("Support Ticket Queue")

    st.caption(
        "Fictional clinic support scenarios for portfolio demonstration."
    )

    st.metric("Tickets in Queue", len(filtered))

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        label="Download Ticket Queue",
        data=filtered.to_csv(index=False),
        file_name="clinic_ticket_queue.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# TAB 3 — SLA MONITORING
# --------------------------------------------------

with sla_tab:
    st.header("Historical SLA Monitoring")

    st.caption(
        "First-response SLA calculations using fictional ticket timestamps."
    )

    met = int(sla["SLA Status"].eq("Met").sum())
    breached = int(sla["SLA Status"].eq("Breached").sum())
    missing = int(
        sla["SLA Status"].eq("Response Not Recorded").sum()
    )

    evaluated = met + breached

    a, b, c = st.columns(3)

    a.metric("SLA Met", met)
    b.metric("SLA Breached", breached)
    c.metric("Response Not Recorded", missing)

    st.metric(
        "First-Response SLA Compliance",
        f"{met / evaluated:.1%}" if evaluated else "N/A"
    )

    st.subheader("Ticket SLA Details")

    display_columns = [
        "ticket_id",
        "clinic",
        "issue_type",
        "priority",
        "first_response_minutes",
        "response_minutes",
        "SLA Status"
    ]

    st.dataframe(
        sla[display_columns],
        use_container_width=True,
        hide_index=True
    )

    if not sla.empty:
        st.subheader("SLA Status Distribution")

        st.bar_chart(
            sla["SLA Status"].value_counts()
        )

    st.subheader("Support Escalation Alerts")

    if breached:
        st.error(
            f"{breached} ticket(s) breached the historical SLA."
        )

    if missing:
        st.warning(
            f"{missing} ticket(s) have no recorded first response."
        )

    for label in [
        "Creation Time Missing/Invalid",
        "Invalid Response Timestamp",
        "Policy Missing"
    ]:
        count = int(sla["SLA Status"].eq(label).sum())

        if count:
            st.warning(
                f"{count} ticket(s): {label}"
            )

    st.download_button(
        label="Download SLA Report",
        data=sla.to_csv(index=False),
        file_name="clinic_sla_report.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# TAB 4 — TICKET ROUTING
# --------------------------------------------------

with routing_tab:
    st.header("Automated Ticket Routing")

    st.caption(
        "Rule-based support team assignments. "
        "Teams are illustrative, not verified vendor structures."
    )

    if filtered.empty:
        st.info("No tickets match the current filters.")

    else:
        routed = pd.DataFrame(
            [
                route_ticket(ticket)
                for ticket in filtered.to_dict(
                    orient="records"
                )
            ]
        )

        r1, r2, r3 = st.columns(3)

        r1.metric("Tickets Routed", len(routed))
        r2.metric(
            "Support Teams",
            routed["assigned_team"].nunique()
        )
        r3.metric(
            "Urgent Tickets",
            int(routed["priority"].eq("Urgent").sum())
        )

        st.subheader("Ticket Assignment Queue")

        st.dataframe(
            routed,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Tickets by Assigned Team")

        st.bar_chart(
            routed["assigned_team"].value_counts()
        )

        st.subheader("Routing Decisions")

        for _, ticket in routed.iterrows():
            st.info(
                f"{ticket['ticket_id']} | "
                f"{ticket['issue_type']} → "
                f"{ticket['assigned_team']}"
            )

        st.download_button(
            label="Download Routing Report",
            data=routed.to_csv(index=False),
            file_name="clinic_ticket_routing.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# TAB 5 — SLA RISK ALERTS
# --------------------------------------------------

with risk_tab:
    st.header("Proactive SLA Risk Alerts")

    st.caption(
        "Interactive hypothetical simulation. "
        "Not real-time monitoring or machine learning."
    )

    if not valid_ids:
        st.info(
            "No valid SLA policies are available for simulation."
        )

    else:
        st.selectbox(
            "Select a Support Ticket",
            options=valid_ids,
            key="sim_ticket_id"
        )

        selected = valid_targets[
            valid_targets["ticket_id"]
            == st.session_state["sim_ticket_id"]
        ].iloc[0]

        target = float(
            selected["first_response_minutes"]
        )

        slider_max = max(
            30,
            int(target * 2),
            int(st.session_state["sim_elapsed"])
        )

        st.write(
            f"**Issue:** {selected['issue_type']} | "
            f"**Priority:** {selected['priority']} | "
            f"**SLA Target:** {target:g} minutes"
        )

        st.slider(
            "Simulated minutes since ticket creation "
            "(no first response yet)",
            min_value=0,
            max_value=slider_max,
            step=1,
            key="sim_elapsed"
        )

        elapsed = st.session_state["sim_elapsed"]

        status = simulation_status(
            elapsed,
            target
        )

        remaining = target - elapsed

        st.progress(
            min(elapsed / target, 1.0)
        )

        m1, m2, m3 = st.columns(3)

        m1.metric("Elapsed Time", f"{elapsed} min")
        m2.metric("SLA Target", f"{target:g} min")
        m3.metric(
            "Time Remaining",
            f"{max(remaining, 0):g} min"
        )

        if status == "BREACHED":
            st.error(
                "BREACHED — The simulated response deadline "
                "has passed."
            )

        elif status == "AT RISK":
            st.warning(
                "AT RISK — At least 80% of the SLA window "
                "has elapsed."
            )

        else:
            st.success(
                "ON TRACK — Below the warning threshold."
            )

        st.subheader("Recommended Support Action")

        st.info(
            simulation_action(status)
        )

        st.subheader("Simulation Result")

        result = pd.DataFrame(
            [
                {
                    "ticket_id": st.session_state["sim_ticket_id"],
                    "priority": selected["priority"],
                    "sla_target_minutes": target,
                    "simulated_elapsed_minutes": elapsed,
                    "remaining_minutes": remaining,
                    "risk_status": status,
                    "recommended_action": simulation_action(status)
                }
            ]
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="Download Risk Simulation",
            data=result.to_csv(index=False),
            file_name="clinic_sla_risk_simulation.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Clinic Support Operations Lab | "
    "Fictional portfolio demonstration | "
    "No real patient data | "
    "No live SLA monitoring or AI predictions"
)
