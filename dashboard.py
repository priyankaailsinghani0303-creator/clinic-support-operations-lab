
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
