"""
Clinic Support Operations Lab - SLA Dashboard
Streamlit app - fictional data only, illustrative SLA targets.
Dashboard design inspired by Arooj Javed's Smart Support Analytics Dashboard
(github.com/aroojjaved93/Smart-support-analytics-dashboard).
Original implementation for this project's fictional clinic data - not a copy.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Clinic Support - SLA Dashboard", layout="wide")
st.title("Support Overview")

# --- Fictional data (same as README / sla_checker.py) ---
# T001: 10 min vs 15 -> MET | T002: 50 min vs 30 -> BREACHED | T003: not recorded -> RESPONSE NOT RECORDED
DATA = [
    {"ticket": "T001", "clinic": "Demo Aesthetic Clinic", "issue": "Booking", "issue_detail": "Booking / Calendar",
     "priority": "Urgent", "status": "Open", "response_min": 10, "sla_target_min": 15, "result": "MET"},
    {"ticket": "T002", "clinic": "Demo Wellness Clinic", "issue": "Payments", "issue_detail": "Payments",
     "priority": "High", "status": "Open", "response_min": 50, "sla_target_min": 30, "result": "BREACHED"},
    {"ticket": "T003", "clinic": "Demo Skin Clinic", "issue": "Messaging", "issue_detail": "Messaging",
     "priority": "Medium", "status": "Open", "response_min": None, "sla_target_min": 120, "result": "RESPONSE NOT RECORDED"},
]
df = pd.DataFrame(DATA)

# --- Sidebar filters (like your screenshot) ---
st.sidebar.header("Filters")
clinics = st.sidebar.multiselect("Clinic", sorted(df["clinic"].unique()), default=sorted(df["clinic"].unique()))
priorities = st.sidebar.multiselect("Priority", ["Urgent", "High", "Medium", "Low"], default=["Urgent", "High", "Medium"])
statuses = st.sidebar.multiselect("Status", sorted(df["status"].unique()), default=sorted(df["status"].unique()))
issues = st.sidebar.multiselect("Issue Type", sorted(df["issue"].unique()), default=sorted(df["issue"].unique()))

filtered = df[
    df["clinic"].isin(clinics)
    & df["priority"].isin(priorities)
    & df["status"].isin(statuses)
    & df["issue"].isin(issues)
].copy()

if filtered.empty:
    st.warning("No tickets match these filters.")
    st.stop()

# --- KPI row (FIX 1: High Priority = High only, NOT Urgent+High) ---
total = len(filtered)
urgent = int((filtered["priority"] == "Urgent").sum())
open_tickets = int((filtered["status"] == "Open").sum())
high_priority = int((filtered["priority"] == "High").sum())  # High only = 1

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tickets", total)
c2.metric("Urgent Tickets", urgent)
c3.metric("Open Tickets", open_tickets)
c4.metric("High Priority", high_priority)
st.caption("High Priority counts priority = High only. Urgent is counted separately.")

# --- SLA Overview (FIX 3: at the top, before the chart) ---
met = int((filtered["result"] == "MET").sum())
breached = int((filtered["result"] == "BREACHED").sum())
missing = int((filtered["result"] == "RESPONSE NOT RECORDED").sum())
evaluated = met + breached
compliance = (met / evaluated * 100) if evaluated else 0.0

st.subheader("SLA Overview")
s1, s2, s3, s4 = st.columns(4)
s1.metric("SLA Met", met)
s2.metric("SLA Breached", breached)
s3.metric("Missing Response", missing)
s4.metric("Compliance", f"{compliance:.1f}%")
st.caption("Missing responses are NOT counted in compliance. They are reported separately from confirmed breaches.")

# --- Tabs ---
tab_overview, tab_queue = st.tabs(["Overview", "Ticket Queue"])

with tab_overview:
    # FIX 2: horizontal bar chart - labels never clip
    order = ["Urgent", "High", "Medium", "Low"]
    counts = filtered["priority"].value_counts().reindex(order).fillna(0).astype(int)
    chart_df = pd.DataFrame({"priority": counts.index, "count": counts.values})
    chart_df = chart_df[chart_df["count"] > 0]
    fig = px.bar(
        chart_df, x="count", y="priority", orientation="h",
        labels={"count": "Tickets", "priority": "Priority"},
        title="Tickets by Priority", text="count",
    )
    fig.update_layout(height=300, margin=dict(l=80, r=20, t=40, b=20), yaxis=dict(categoryorder="array", categoryarray=["Low", "Medium", "High", "Urgent"]))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Fictional data. SLA targets are illustrative, not a real clinic contract.")

with tab_queue:
    # Breached first, then Missing, then Met
    rank = {"BREACHED": 0, "RESPONSE NOT RECORDED": 1, "MET": 2}
    queue = filtered.copy()
    queue["_rank"] = queue["result"].map(rank)
    queue = queue.sort_values(["_rank", "ticket"]).drop(columns=["_rank"])
    queue["Response Time"] = queue["response_min"].apply(lambda x: f"{int(x)} min" if pd.notna(x) else "Not recorded")
    queue["SLA Target"] = queue["sla_target_min"].apply(lambda x: f"{int(x)} min")
    queue["Action"] = queue["result"].map({
        "MET": "Continue normal follow-up.",
        "BREACHED": "Review SLA breach, update clinic, notify support lead.",
        "RESPONSE NOT RECORDED": "Verify response history and contact clinic if needed.",
    })
    st.dataframe(
        queue[["ticket", "clinic", "issue_detail", "priority", "status", "Response Time", "SLA Target", "result", "Action"]]
        .rename(columns={"ticket": "Ticket", "clinic": "Clinic", "issue_detail": "Issue", "priority": "Priority",
                 "status": "Status", "result": "Result"}),
        use_container_width=True, hide_index=True,
    )

# --- Footer / attribution ---
st.divider()
st.caption("Dashboard design inspired by Arooj Javed's Smart Support Analytics Dashboard (github.com/aroojjaved93/Smart-support-analytics-dashboard). Original implementation for fictional clinic data - not a copy.")
st.caption("Fictional data. Illustrative SLA targets only. Elapsed-time calculation. No real patient data.")
