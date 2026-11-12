import pandas as pd
import streamlit as st

st.set_page_config(page_title="Clinic Support - SLA Dashboard", layout="wide")
st.title("Support Overview")

DATA = [
    {"Ticket": "T001", "Clinic": "Demo Aesthetic Clinic", "Issue": "Booking / Calendar", "Priority": "Urgent", "Status": "Open", "Response Time": "10 min", "SLA Target": "15 min", "Result": "MET"},
    {"Ticket": "T002", "Clinic": "Demo Wellness Clinic", "Issue": "Payments", "Priority": "High", "Status": "Open", "Response Time": "50 min", "SLA Target": "30 min", "Result": "BREACHED"},
    {"Ticket": "T003", "Clinic": "Demo Skin Clinic", "Issue": "Messaging", "Priority": "Medium", "Status": "Open", "Response Time": "Not recorded", "SLA Target": "120 min", "Result": "RESPONSE NOT RECORDED"},
]
df = pd.DataFrame(DATA)

st.sidebar.header("Filters")
clinics = st.sidebar.multiselect("Clinic", sorted(df["Clinic"].unique()), default=sorted(df["Clinic"].unique()))
priorities = st.sidebar.multiselect("Priority", ["Urgent", "High", "Medium", "Low"], default=["Urgent", "High", "Medium"])
statuses = st.sidebar.multiselect("Status", sorted(df["Status"].unique()), default=sorted(df["Status"].unique()))
issues = st.sidebar.multiselect("Issue Type", sorted(df["Issue"].unique()), default=sorted(df["Issue"].unique()))
filtered = df[df["Clinic"].isin(clinics) & df["Priority"].isin(priorities) & df["Status"].isin(statuses) & df["Issue"].isin(issues)].copy()
if filtered.empty:
    st.warning("No tickets match these filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tickets", len(filtered))
c2.metric("Urgent Tickets", int((filtered["Priority"] == "Urgent").sum()))
c3.metric("Open Tickets", int((filtered["Status"] == "Open").sum()))
c4.metric("High Priority", int((filtered["Priority"] == "High").sum()))
st.caption("High Priority = High only, not Urgent+High.")

met = int((filtered["Result"] == "MET").sum())
breached = int((filtered["Result"] == "BREACHED").sum())
missing = int((filtered["Result"] == "RESPONSE NOT RECORDED").sum())
compliance = (met / (met + breached) * 100) if (met + breached) else 0.0
st.subheader("SLA Overview")
s1, s2, s3, s4 = st.columns(4)
s1.metric("SLA Met", met)
s2.metric("SLA Breached", breached)
s3.metric("Missing Response", missing)
s4.metric("Compliance", f"{compliance:.1f}%")
st.caption("Missing responses are NOT counted in compliance.")

tab1, tab2 = st.tabs(["Overview", "Ticket Queue"])
with tab1:
    st.subheader("Tickets by Priority")
    st.bar_chart(filtered["Priority"].value_counts())
with tab2:
    rank = {"BREACHED": 0, "RESPONSE NOT RECORDED": 1, "MET": 2}
    q = filtered.copy()
    q["_r"] = q["Result"].map(rank)
    q = q.sort_values(["_r", "Ticket"]).drop(columns=["_r"])
    q["Action"] = q["Result"].map({"MET": "Continue normal follow-up.", "BREACHED": "Review SLA breach, update clinic, notify support lead.", "RESPONSE NOT RECORDED": "Verify response history and contact clinic if needed."})
    st.dataframe(q, use_container_width=True, hide_index=True)

st.divider()
st.caption("Dashboard design inspired by Arooj Javed's Smart Support Analytics Dashboard (github.com/aroojjaved93/Smart-support-analytics-dashboard). Original implementation for fictional clinic data - not a copy.")
st.caption("Fictional data. Illustrative SLA targets only. No real patient data.")
