from pathlib import Path

import pandas as pd
import streamlit as st

from support_rules import calculate_sla, route_ticket, simulation_status, simulation_action


st.set_page_config(
    page_title="Clinic Support Operations Lab",
    page_icon="🏥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

st.title("🏥 Clinic Support Operations Lab")
st.caption(
    "Healthcare SaaS support portfolio · Fictional clinic scenarios · "
    "Rule-based workflow demonstration"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_csv(filename):
    path = BASE_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()


tickets = load_csv("tickets.csv")
timestamps = load_csv("ticket_timestamps.csv")
policies = load_csv("sla_policy.csv")

required_columns = {
    "ticket_id",
    "clinic",
    "issue_type",
    "priority",
    "status",
    "description",
}

if tickets.empty:
    st.error("tickets.csv is missing or empty.")
    st.stop()

missing_columns = required_columns - set(tickets.columns)

if missing_columns:
    st.error(
        "Missing ticket columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

tickets = tickets.copy()

for column in required_columns:
    tickets[column] = (
        tickets[column].fillna("").astype(str).str.strip()
    )

for column in ["priority", "status", "issue_type"]:
    tickets[column] = tickets[column].str.title()

if tickets["ticket_id"].eq("").any():
    st.error("Every ticket must have a ticket_id.")
    st.stop()

if tickets["ticket_id"].duplicated().any():
    st.error("Duplicate ticket IDs found in tickets.csv.")
    st.stop()


# --------------------------------------------------
# HISTORICAL SLA CALCULATIONS
# --------------------------------------------------

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Ticket Filters")

filtered = tickets.copy()

for column, label in [
    ("clinic", "Clinic"),
    ("priority", "Priority"),
    ("status", "Status"),
    ("issue_type", "Issue Type"),
]:
    options = sorted(tickets[column].unique().tolist())

    selected = st.sidebar.multiselect(
        label,
        options,
        default=options,
        key=f"filter_{column}",
    )

    filtered = filtered[
        filtered[column].isin(selected)
    ].copy()

sla = calculate_sla(filtered, timestamps, policies)

met_count = int(sla["SLA Status"].eq("Met").sum())
breached_count = int(
    sla["SLA Status"].eq("Breached").sum()
)
unevaluated_count = int(
    (~sla["SLA Status"].isin(["Met", "Breached"])).sum()
)

evaluated_count = met_count + breached_count

compliance = (
    f"{met_count / evaluated_count:.1%}"
    if evaluated_count
    else "N/A"
)


# --------------------------------------------------
# ROUTING
# --------------------------------------------------

valid_targets = sla[
    sla["first_response_minutes"].notna()
].copy()


# --------------------------------------------------
# TABS
# --------------------------------------------------

overview_tab, queue_tab, sla_tab, routing_tab, risk_tab = (
    st.tabs(
        [
            "Overview",
            "Ticket Queue",
            "SLA Monitoring",
            "Ticket Routing",
            "SLA Risk Alerts",
        ]
    )
)


# --------------------------------------------------
# TAB 1 — OVERVIEW
# --------------------------------------------------

with overview_tab:
    st.header("Support Operations Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", len(filtered))
    c2.metric(
        "Open Tickets",
        int(filtered["status"].eq("Open").sum()),
    )
    c3.metric(
        "Urgent Tickets",
        int(filtered["priority"].eq("Urgent").sum()),
    )
    c4.metric(
        "High Priority",
        int(filtered["priority"].eq("High").sum()),
    )

    if filtered.empty:
        st.info("No tickets match the selected filters.")
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

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("SLA Met", met_count)
    s2.metric("SLA Breached", breached_count)
    s3.metric("Cannot Evaluate SLA", unevaluated_count)
    s4.metric("SLA Compliance", compliance)

    st.caption(
        f"Compliance uses {evaluated_count} evaluable ticket(s). "
        "Tickets with missing or invalid data or policies are excluded. "
        "All records are fictional."
    )

    if unevaluated_count:
        st.warning(
            f"{unevaluated_count} ticket(s) cannot be evaluated. "
            "Open SLA Monitoring to see the specific reasons."
        )

    st.info(
        "Meeting a first-response SLA does not mean the issue "
        "has been resolved."
    )


# --------------------------------------------------
# TAB 2 — TICKET QUEUE
# --------------------------------------------------

with queue_tab:
    st.header("Support Ticket Queue")
    st.caption("Fictional clinic support scenarios.")

    st.metric("Tickets in Queue", len(filtered))
    if "assigned_owner" in filtered:
        unassigned = filtered["assigned_owner"].fillna("").astype(str).str.strip().eq("")
        st.metric("Owner Not Assigned", int(unassigned.sum()))
        if unassigned.any():
            st.info("Fictional records have no accepted named owner. Operational tickets require one accountable owner.")

    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download Ticket Queue",
        data=filtered.to_csv(index=False),
        file_name="clinic_ticket_queue.csv",
        mime="text/csv",
        key="download_queue",
    )


# --------------------------------------------------
# TAB 3 — SLA MONITORING
# --------------------------------------------------

with sla_tab:
    st.header("Historical SLA Monitoring")

    st.caption(
        "First-response calculations use elapsed minutes. "
        "Naive timestamps are interpreted as UTC. "
        "Business-hour schedules and resolution SLAs are not calculated."
    )

    a, b, c = st.columns(3)

    a.metric("SLA Met", met_count)
    b.metric("SLA Breached", breached_count)
    c.metric("Cannot Evaluate SLA", unevaluated_count)

    st.metric(
        "First-Response SLA Compliance",
        compliance,
    )

    st.subheader("Ticket SLA Details")

    display_columns = [
        "ticket_id",
        "clinic",
        "issue_type",
        "priority",
        "created_at",
        "first_responded_at",
        "first_response_minutes",
        "response_minutes",
        "SLA Status",
    ]

    st.dataframe(
        sla[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    if not sla.empty:
        st.subheader("SLA Status Distribution")
        st.bar_chart(sla["SLA Status"].value_counts())

    st.subheader("Review Alerts")

    if breached_count:
        st.error(
            f"{breached_count} ticket(s) exceeded the recorded "
            "first-response target. Review the delay and follow-up."
        )

    unevaluated = sla[
        ~sla["SLA Status"].isin(["Met", "Breached"])
    ]

    for label, count in (
        unevaluated["SLA Status"].value_counts().items()
    ):
        st.warning(f"{count} ticket(s): {label}")

    if filtered.empty:
        st.info("No tickets match the selected filters.")
    elif not breached_count and not unevaluated_count:
        st.success(
            "All selected tickets have evaluable responses "
            "within their targets."
        )

    with st.expander("How to interpret these statuses"):
        st.markdown(
            """
- **Met:** Recorded response was within the target.
- **Breached:** Recorded response exceeded the target.
- **Response Not Recorded:** Creation time is valid, but the
  response timestamp is absent.
- **Creation Time Missing/Invalid:** The starting time is unknown.
- **Invalid Response Timestamp:** The response is unparseable
  or earlier than creation.
- **Policy Missing/Invalid:** No unique, positive, finite target
  is available.
- **Duplicate Timestamp Records:** More than one timestamp row
  exists for the ticket.

**Cannot Evaluate SLA** groups every status other than Met or Breached.

This historical report does not calculate whether an unanswered
ticket has passed its deadline as of the current time.
            """
        )

    st.download_button(
        "Download SLA Report",
        data=sla[display_columns].to_csv(index=False),
        file_name="clinic_sla_report.csv",
        mime="text/csv",
        key="download_sla",
    )


# --------------------------------------------------
# TAB 4 — TICKET ROUTING
# --------------------------------------------------

with routing_tab:
    st.header("Suggested Ticket Routing")

    st.caption(
        "Rule-based initial ownership suggestions. "
        "Teams are illustrative. Escalation depends on findings "
        "and business impact."
    )

    if filtered.empty:
        st.info("No tickets match the selected filters.")
    else:
        routed = pd.DataFrame(
            [
                route_ticket(ticket)
                for ticket in filtered.to_dict(
                    orient="records"
                )
            ]
        )

        r1, r2 = st.columns(2)

        r1.metric("Routing Suggestions", len(routed))
        r2.metric(
            "Suggested Teams",
            routed["suggested_initial_team"].nunique(),
        )

        st.dataframe(
            routed,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Tickets by Suggested Initial Team")
        st.bar_chart(
            routed["suggested_initial_team"].value_counts()
        )

        st.download_button(
            "Download Routing Report",
            data=routed.to_csv(index=False),
            file_name="clinic_ticket_routing.csv",
            mime="text/csv",
            key="download_routing",
        )


# --------------------------------------------------
# TAB 5 — SLA RISK ALERTS
# --------------------------------------------------

with risk_tab:
    st.header("Hypothetical SLA Risk Alerts")

    st.caption(
        "Simulation only. Assumes the selected ticket has not "
        "received a first response. It does not change historical results."
    )

    if valid_targets.empty:
        st.info(
            "No selected tickets have a valid SLA target "
            "for simulation."
        )
    else:
        valid_ids = valid_targets["ticket_id"].tolist()

        if st.session_state.get("risk_ticket") not in valid_ids:
            st.session_state["risk_ticket"] = valid_ids[0]

        selected_id = st.selectbox(
            "Select a Support Ticket",
            options=valid_ids,
            key="risk_ticket",
        )

        selected = valid_targets[
            valid_targets["ticket_id"].eq(selected_id)
        ].iloc[0]

        target = float(selected["first_response_minutes"])

        st.write(
            f"**Issue:** {selected['issue_type']} · "
            f"**Priority:** {selected['priority']} · "
            f"**Target:** {target:g} minutes"
        )

        elapsed = st.slider(
            "Simulated elapsed minutes with no first response",
            min_value=0,
            max_value=max(30, int(target * 2)),
            value=0,
            step=1,
            key=f"elapsed_{selected_id}_{target:g}",
        )

        risk_status = simulation_status(elapsed, target)
        remaining = max(target - elapsed, 0)

        st.progress(min(elapsed / target, 1.0))

        m1, m2, m3 = st.columns(3)

        m1.metric("Elapsed", f"{elapsed} min")
        m2.metric("Target", f"{target:g} min")
        m3.metric("Time Remaining", f"{remaining:g} min")

        if risk_status == "BREACHED":
            st.error("BREACHED — Simulated deadline has passed.")
        elif risk_status == "AT RISK":
            st.warning(
                "AT RISK — At least 80% of the response "
                "window has elapsed."
            )
        else:
            st.success("ON TRACK — Below the warning threshold.")

        st.subheader("Recommended Action")
        st.info(simulation_action(risk_status))

        simulation_result = pd.DataFrame(
            [
                {
                    "ticket_id": selected_id,
                    "priority": selected["priority"],
                    "sla_target_minutes": target,
                    "simulated_elapsed_minutes": elapsed,
                    "remaining_minutes": remaining,
                    "risk_status": risk_status,
                    "recommended_action": simulation_action(
                        risk_status
                    ),
                }
            ]
        )

        st.download_button(
            "Download Risk Simulation",
            data=simulation_result.to_csv(index=False),
            file_name="clinic_sla_risk_simulation.csv",
            mime="text/csv",
            key="download_simulation",
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Clinic Support Operations Lab · Independent fictional portfolio "
    "demonstration · No real patient data · "
    "No live monitoring or AI predictions"
)

