import streamlit as st
from datetime import datetime
from appointment import CategoryAppointment
from notifications import add_notification
from views.shared_views import show_all_appointments_view, show_dashboard_view


def show_noc_views(user, app_mode):
    if app_mode == "✅ NOC Approvals":
        show_noc_approvals(user)
    elif app_mode == "📊 All Appointments":
        show_all_appointments_view()
    elif app_mode == "📈 Dashboard":
        show_dashboard_view()


def show_noc_approvals(user):
    st.header("✅ NOC Appointment Approvals")
    pending_approvals = [a for a in st.session_state.category_appointments
                         if a['noc_approval'] in ['Pending', 'On Hold']]
    st.metric("Pending NOC Approvals", len(pending_approvals))

    if pending_approvals:
        for appt in pending_approvals:
            with st.expander(f"📋 ISA: {appt['ISA']} - {appt['vendor_name']} | {appt['category']} @ {appt['fc']}", expanded=True):
                col_info, col_action = st.columns([2, 1])
                with col_info:
                    st.write(f"**ISA ID:** {appt['ISA']}")
                    st.write(f"**Vendor:** {appt['vendor_name']} (Code: {appt['vendor_code']})")
                    st.write(f"**FC:** {appt['fc']} | **Category:** {appt['category']}")
                    st.write(f"**Units:** {appt['units']:,} | **Cartons:** {appt['cartons']}")
                    st.write(f"**Scheduled:** {appt['appt_date']} | **Requested:** {appt['prepone_date']}")
                    st.write(f"**Lead Time:** {appt['lead_time']} hours")
                    st.write(f"**Seller Remarks:** {appt['ibsc_remarks']}")
                    if appt.get('ibsc_team_remarks'):
                        st.info(f"💬 **IBSC Team Remarks:** {appt['ibsc_team_remarks']}")
                with col_action:
                    st.write(f"**IBSC Status:** {appt['ibsc_approval']}")
                    st.write(f"**Current NOC Status:** {appt['noc_approval']}")

                st.markdown("---")
                noc_col1, noc_col2 = st.columns(2)
                with noc_col1:
                    revised_date = st.date_input(
                        "Revised Date (Optional)",
                        value=appt['prepone_date'] if isinstance(appt['prepone_date'], datetime) else datetime.now(),
                        key=f"revised_date_{appt['id']}"
                    )
                with noc_col2:
                    noc_remarks = st.text_area(
                        "NOC Remarks (Optional)", placeholder="Enter scheduling notes...",
                        key=f"noc_remarks_{appt['id']}"
                    )

                col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
                with col_btn1:
                    if st.button("✅ Approve & Execute", key=f"noc_approve_{appt['id']}", type="primary"):
                        CategoryAppointment.update_approval(
                            appt['id'], 'NOC', 'Approved', user['name'],
                            revised_date=revised_date if revised_date != appt['prepone_date'] else None,
                            noc_remarks=noc_remarks or None
                        )
                        st.success("✅ Approved & Executed!")
                        st.rerun()
                with col_btn2:
                    if st.button("⏸️ On Hold", key=f"noc_hold_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'NOC', 'On Hold', user['name'],
                                                            noc_remarks=noc_remarks or None)
                        st.info("⏸️ On Hold")
                        st.rerun()
                with col_btn3:
                    if st.button("❌ Reject", key=f"noc_reject_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'NOC', 'Rejected', user['name'],
                                                            noc_remarks=noc_remarks or None)
                        st.error("❌ Rejected")
                        st.rerun()
                with col_btn4:
                    if st.button("🔄 Reset", key=f"noc_reset_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'NOC', 'Pending', user['name'])
                        st.info("🔄 Reset")
                        st.rerun()
                with col_btn5:
                    _render_slot_override_section(appt, user)
    else:
        st.success("✅ No pending NOC approvals!")


def _render_slot_override_section(appt, user):
    if appt['ibsc_approval'] == 'Approved' and not appt.get('slot_override_requested'):
        if st.button("🔄 Request Slot Override", key=f"noc_override_{appt['id']}"):
            st.session_state[f'show_override_dialog_{appt["id"]}'] = True

    if st.session_state.get(f'show_override_dialog_{appt["id"]}', False):
        st.markdown("---")
        st.warning("**Request Slot Override from IBSC**")
        override_reason = st.text_area(
            "Reason for Slot Override",
            placeholder="Explain why slot override is needed...",
            key=f"override_reason_{appt['id']}", height=100
        )
        col_send, col_cancel = st.columns(2)
        with col_send:
            if st.button("📤 Send Request to IBSC", key=f"send_override_{appt['id']}", type="primary"):
                if override_reason:
                    success = st.session_state.db.request_slot_override(appt['id'], override_reason, user['name'])
                    if success:
                        st.session_state.category_appointments = st.session_state.db.get_all_appointments()
                        add_notification(
                            f"🔄 Slot Override Requested: ISA {appt['ISA']} - {appt['vendor_name']} by {user['name']}",
                            "warning"
                        )
                        st.success("✅ Slot override request sent to IBSC!")
                        st.session_state[f'show_override_dialog_{appt["id"]}'] = False
                        st.rerun()
                else:
                    st.error("Please provide a reason for the override request")
        with col_cancel:
            if st.button("❌ Cancel", key=f"cancel_override_{appt['id']}"):
                st.session_state[f'show_override_dialog_{appt["id"]}'] = False
                st.rerun()

    if appt.get('slot_override_requested'):
        st.markdown("---")
        override_status = appt.get('slot_override_status', 'Pending')
        if override_status == 'Pending':
            st.info("🔄 **Slot Override Status:** Waiting for IBSC response")
            st.caption(f"Reason: {appt.get('slot_override_reason', 'N/A')}")
        elif override_status == 'Approved':
            st.success("✅ **Slot Override Approved by IBSC**")
            if appt.get('slot_override_ibsc_response'):
                st.caption(f"IBSC Response: {appt['slot_override_ibsc_response']}")
            st.info("You can now proceed with final approval")
        elif override_status == 'Rejected':
            st.error("❌ **Slot Override Rejected by IBSC**")
            if appt.get('slot_override_ibsc_response'):
                st.caption(f"IBSC Response: {appt['slot_override_ibsc_response']}")
