
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Clinic Support Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinic Support Operations Dashboard")
st.caption("Portfolio demonstration using fictional clinic tickets")

tickets = pd.read_csv("tickets.csv")

st.subheader("Support Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", len(tickets))
col2.metric("Urgent Tickets", (tickets["priority"] == "Urgent").sum())
col3.metric("Open Tickets", (tickets["status"] == "Open").sum())

st.subheader("Support Ticket Queue")
st.dataframe(tickets, use_container_width=True)

