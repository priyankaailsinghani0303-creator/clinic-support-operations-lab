import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Clinic Support Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Clinic Support Operations Dashboard")
st.caption("Portfolio demonstration using fictional clinic tickets")


@st.cache_data
def load_tickets():
    csv_path = Path(__file__).resolve().parent / "tickets.csv"

    try:
        tickets = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"CSV file not found: {csv_path}")
        return pd.DataFrame()

    required_columns = {
        "ticket_id",
        "clinic",
        "issue_type",
        "priority",
        "status",
        "description",
    }
    missing = required_columns - set(tickets.columns)
    if missing:
        st.error(f"Missing required columns: {sorted(missing)}")
        return pd.DataFrame()

    tickets["clinic"] = tickets["clinic"].astype(str).str.title()
    tickets["issue_type"] = tickets["issue_type"].astype(str).str.title()
    tickets["priority"] = tickets["priority"].astype(str).str.title()
    tickets["status"] = tickets["status"].astype(str).str.title()

    return tickets


tickets = load_tickets()

if tickets.empty:
    st.stop()

st.sidebar.header("Filters")
selected_clinics = st.sidebar.multiselect(
    "Clinic",
    options=sorted(tickets["clinic"].unique()),
    default=sorted(tickets["clinic"].unique()),
)
selected_priorities = st.sidebar.multiselect(
    "Priority",
    options=sorted(tickets["priority"].unique()),
    default=sorted(tickets["priority"].unique()),
)
selected_statuses = st.sidebar.multiselect(
    "Status",
    options=sorted(tickets["status"].unique()),
    default=sorted(tickets["status"].unique()),
)
selected_issue_types = st.sidebar.multiselect(
    "Issue Type",
    options=sorted(tickets["issue_type"].unique()),
    default=sorted(tickets["issue_type"].unique()),
)

filtered_tickets = tickets[
    tickets["clinic"].isin(selected_clinics)
    & tickets["priority"].isin(selected_priorities)
    & tickets["status"].isin(selected_statuses)
    & tickets["issue_type"].isin(selected_issue_types)
].copy()

st.subheader("Support Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(filtered_tickets))
col2.metric("Urgent Tickets", int((filtered_tickets["priority"] == "Urgent").sum()))
col3.metric("Open Tickets", int((filtered_tickets["status"] == "Open").sum()))
col4.metric(
    "High Priority",
    int((filtered_tickets["priority"].isin(["High", "Urgent"])) .sum()),
)

overview_tab, queue_tab = st.tabs(["Overview", "Ticket Queue"])

with overview_tab:
    left_col, right_col = st.columns(2)

    priority_counts = filtered_tickets["priority"].value_counts().reset_index()
    priority_counts.columns = ["priority", "count"]
    left_col.bar_chart(priority_counts.set_index("priority"), use_container_width=True)

    status_counts = filtered_tickets["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    right_col.bar_chart(status_counts.set_index("status"), use_container_width=True)

    clinic_counts = filtered_tickets["clinic"].value_counts().reset_index()
    clinic_counts.columns = ["clinic", "count"]
    st.bar_chart(clinic_counts.set_index("clinic"), use_container_width=True)

    type_counts = filtered_tickets["issue_type"].value_counts().reset_index()
    type_counts.columns = ["issue_type", "count"]
    st.bar_chart(type_counts.set_index("issue_type"), use_container_width=True)

with queue_tab:
    st.dataframe(filtered_tickets, use_container_width=True, hide_index=True)
    
with sla_tab:
    st.subheader("First-Response SLA Monitoring")
    st.caption("Fictional ticket data. SLA targets are demonstration policies.")

    policy = pd.read_csv(
        Path(__file__).resolve().parent / "sla_policy.csv"
    )
    timestamps = pd.read_csv(
        Path(__file__).resolve().parent / "ticket_timestamps.csv"
    )

    sla_data = filtered_tickets.merge(
        policy[["priority", "first_response_minutes"]],
        on="priority",
        how="left"
    ).merge(
        timestamps[["ticket_id", "created_at", "first_responded_at"]],
        on="ticket_id",
        how="left"
    )

    created = pd.to_datetime(sla_data["created_at"], errors="coerce")
    responded = pd.to_datetime(
        sla_data["first_responded_at"], errors="coerce"
    )

    sla_data["response_minutes"] = (
        responded - created
    ).dt.total_seconds() / 60

    def sla_status(row):
        if pd.isna(row["first_response_minutes"]):
            return "Policy Missing"
        if pd.isna(row["response_minutes"]):
            return "Response Not Recorded"
        if row["response_minutes"] < 0:
            return "Invalid Timestamp"
        if row["response_minutes"] <= row["first_response_minutes"]:
            return "Met"
        return "Breached"

    sla_data["SLA Status"] = sla_data.apply(sla_status, axis=1)

    met = (sla_data["SLA Status"] == "Met").sum()
    breached = (sla_data["SLA Status"] == "Breached").sum()
    missing = (sla_data["SLA Status"] == "Response Not Recorded").sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("SLA Met", int(met))
    c2.metric("SLA Breached", int(breached))
    c3.metric("Response Not Recorded", int(missing))

    evaluated = met + breached
    if evaluated:
        st.metric("SLA Compliance", f"{met / evaluated:.0%}")

    st.dataframe(
        sla_data[
            [
                "ticket_id",
                "issue_type",
                "priority",
                "first_response_minutes",
                "response_minutes",
                "SLA Status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    if breached:
        st.error(f"{breached} ticket(s) breached the first-response SLA.")

    if missing:
        st.warning(
            f"{missing} ticket(s) have no recorded first response. "
            "Verify the response history."
        )

