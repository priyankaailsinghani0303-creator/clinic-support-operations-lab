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

    required_columns = {"priority", "status"}
    missing = required_columns - set(tickets.columns)
    if missing:
        st.error(f"Missing required columns: {sorted(missing)}")
        return pd.DataFrame()

    return tickets

tickets = load_tickets()

if tickets.empty:
    st.stop()

tickets["priority"] = tickets["priority"].astype(str).str.title()
tickets["status"] = tickets["status"].astype(str).str.title()

st.subheader("Support Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", len(tickets))
col2.metric("Urgent Tickets", (tickets["priority"] == "Urgent").sum())
col3.metric("Open Tickets", (tickets["status"] == "Open").sum())

st.subheader("Support Ticket Queue")
st.dataframe(tickets, use_container_width=True)
