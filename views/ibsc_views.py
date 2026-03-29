import streamlit as st
from datetime import datetime
from appointment import CategoryAppointment
from notifications import add_notification, broadcast_notification
from views.shared_views import show_all_appointments_view, show_dashboard_view


def show_ibsc_views(user, app_mode):
    if app_mode == "✅ IBSC Approvals":
        show_ibsc_approvals(user)
    elif app_mode == "🔄 Slot Override Requests":
        show_slot_override_requests(user)
    elif app_mode == "📊 All Appointments":
        show_all_appointments_view()
    elif app_mode == "📈 Dashboard":
        show_dashboard_view()


def show_ibsc_approvals(user):
    st.header("✅ IBSC Appointment Approvals")
    pending_approvals = [a for a in st.session_state.category_appointments
                         if a['ibsc_approval'] in ['Pending', 'On Hold']]
    st.metric("Pending IBSC Approvals", len(pending_approvals))

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
                    st.caption(f"Created: {appt['created_at'].strftime('%Y-%m-%d %H:%M')}")
                with col_action:
                    st.write(f"**Current Status:** {appt['ibsc_approval']}")
                    st.write(f"**NOC Status:** {appt['noc_approval']}")

                st.markdown("---")
                ibsc_remarks_input = st.text_area(
                    "IBSC Remarks (Optional)", placeholder="Enter IBSC team remarks...",
                    key=f"ibsc_remarks_{appt['id']}", height=80
                )
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                with col_btn1:
                    if st.button("✅ Approve", key=f"ibsc_approve_{appt['id']}", type="primary"):
                        CategoryAppointment.update_approval(appt['id'], 'IBSC', 'Approved', user['name'],
                                                            ibsc_team_remarks=ibsc_remarks_input or None)
                        st.success("✅ Approved!")
                        st.rerun()
                with col_btn2:
                    if st.button("⏸️ On Hold", key=f"ibsc_hold_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'IBSC', 'On Hold', user['name'],
                                                            ibsc_team_remarks=ibsc_remarks_input or None)
                        st.info("⏸️ On Hold")
                        st.rerun()
                with col_btn3:
                    if st.button("❌ Reject", key=f"ibsc_reject_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'IBSC', 'Rejected', user['name'],
                                                            ibsc_team_remarks=ibsc_remarks_input or None)
                        st.error("❌ Rejected")
                        st.rerun()
                with col_btn4:
                    if st.button("🔄 Reset", key=f"ibsc_reset_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'IBSC', 'Pending', user['name'])
                        st.info("🔄 Reset")
                        st.rerun()
    else:
        st.success("✅ No pending IBSC approvals!")


def show_slot_override_requests(user):
    st.header("🔄 Slot Override Requests from NOC")
    override_requests = st.session_state.db.get_slot_override_requests()
    st.metric("Pending Override Requests", len(override_requests))

    if override_requests:
        for appt in override_requests:
            with st.expander(f"🔄 ISA: {appt['ISA']} - {appt['vendor_name']} | Override Requested", expanded=True):
                col_info, col_status = st.columns([2, 1])
                with col_info:
                    st.write(f"**ISA ID:** {appt['ISA']}")
                    st.write(f"**Vendor:** {appt['vendor_name']} (Code: {appt['vendor_code']})")
                    st.write(f"**FC:** {appt['fc']} | **Category:** {appt['category']}")
                    st.write(f"**Units:** {appt['units']:,} | **Cartons:** {appt['cartons']}")
                    st.write(f"**Scheduled Date:** {appt['appt_date']}")
                with col_status:
                    st.write(f"**IBSC Status:** {appt['ibsc_approval']}")
                    st.write(f"**NOC Status:** {appt['noc_approval']}")
                    st.write(f"**Override Status:** {appt.get('slot_override_status', 'Pending')}")

                st.markdown("---")
                st.warning(f"**NOC Override Reason:** {appt.get('slot_override_reason', 'No reason provided')}")
                if appt.get('slot_override_requested_at'):
                    st.caption(f"Requested: {appt['slot_override_requested_at'].strftime('%Y-%m-%d %H:%M')}")

                ibsc_response = st.text_area(
                    "IBSC Response (Optional)", placeholder="Enter your response...",
                    key=f"override_response_{appt['id']}", height=80
                )
                col_approve, col_reject = st.columns(2)
                with col_approve:
                    if st.button("✅ Approve Override", key=f"override_approve_{appt['id']}", type="primary"):
                        success = st.session_state.db.respond_slot_override(appt['id'], 'Approved', user['name'], ibsc_response)
                        if success:
                            st.session_state.category_appointments = st.session_state.db.get_all_appointments()
                            broadcast_notification(f"Slot Override Approved: ISA {appt['ISA']} - {appt['vendor_name']}",
                                                   "success", vendor_name=appt['vendor_name'])
                            st.success("✅ Slot override approved!")
                            st.rerun()
                with col_reject:
                    if st.button("❌ Reject Override", key=f"override_reject_{appt['id']}"):
                        success = st.session_state.db.respond_slot_override(appt['id'], 'Rejected', user['name'], ibsc_response)
                        if success:
                            st.session_state.category_appointments = st.session_state.db.get_all_appointments()
                            broadcast_notification(f"Slot Override Rejected: ISA {appt['ISA']} - {appt['vendor_name']}",
                                                   "warning", vendor_name=appt['vendor_name'])
                            st.error("❌ Slot override rejected")
                            st.rerun()
    else:
        st.info("No pending slot override requests")
