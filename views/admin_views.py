import streamlit as st
import pandas as pd
from datetime import datetime
from appointment import CategoryAppointment
from views.shared_views import show_all_appointments_view, show_dashboard_view


def show_admin_views(user, app_mode):
    if app_mode == "📊 All Appointments":
        show_all_appointments_view()
    elif app_mode == "✅ Approval Management":
        show_approval_management(user)
    elif app_mode == "📈 Dashboard":
        show_dashboard_view()
    elif app_mode == "📜 Activity Logs":
        show_activity_logs()


def show_approval_management(user):
    st.header("✅ Approval Management (Admin)")
    pending_approvals = CategoryAppointment.get_pending_approvals()

    col_metric1, col_metric2, col_metric3 = st.columns(3)
    col_metric1.metric("Pending Approvals", len(pending_approvals))
    col_metric2.metric("Total Appointments", len(st.session_state.category_appointments))
    col_metric3.metric("Executed Today", len([
        a for a in st.session_state.category_appointments
        if a['status'] == 'Executed' and a['created_at'].date() == datetime.now().date()
    ]))
    st.markdown("---")

    if pending_approvals:
        for appt in pending_approvals:
            with st.expander(f"📋 ISA: {appt['ISA']} - {appt['vendor_name']} | {appt['category']} @ {appt['fc']}"):
                col_info, col_approval = st.columns([2, 1])
                with col_info:
                    st.write(f"**ISA ID:** {appt['ISA']}")
                    st.write(f"**Vendor:** {appt['vendor_name']} ({appt['vendor_code']})")
                    st.write(f"**FC:** {appt['fc']} | **Category:** {appt['category']}")
                    st.write(f"**Units:** {appt['units']:,} | **Cartons:** {appt['cartons']}")
                    st.write(f"**Scheduled:** {appt['appt_date']} | **Requested:** {appt['prepone_date']}")
                    st.write(f"**Lead Time:** {appt['lead_time']} hours")
                    st.write(f"**Seller Remarks:** {appt['ibsc_remarks']}")
                    if appt.get('ibsc_team_remarks'):
                        st.info(f"💬 **IBSC Team Remarks:** {appt['ibsc_team_remarks']}")
                    if appt.get('noc_remarks'):
                        st.info(f"💬 **NOC Team Remarks:** {appt['noc_remarks']}")
                with col_approval:
                    st.write(f"**IBSC:** {appt['ibsc_approval']}")
                    st.write(f"**NOC:** {appt['noc_approval']}")
                    st.write(f"**Status:** {appt['status']}")

                st.markdown("---")
                col_ibsc, col_noc = st.columns(2)
                with col_ibsc:
                    st.markdown("**IBSC Approval**")
                    ibsc_action = st.selectbox("Action", ['Pending', 'On Hold', 'Approved', 'Rejected'],
                                               key=f"admin_ibsc_{appt['id']}")
                    if st.button("Update IBSC", key=f"admin_ibsc_btn_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'IBSC', ibsc_action, user['username'])
                        st.success(f"✅ IBSC updated to {ibsc_action}")
                        st.rerun()
                with col_noc:
                    st.markdown("**NOC Approval**")
                    noc_action = st.selectbox("Action", ['Pending', 'On Hold', 'Approved', 'Rejected'],
                                              key=f"admin_noc_{appt['id']}")
                    if st.button("Update NOC", key=f"admin_noc_btn_{appt['id']}"):
                        CategoryAppointment.update_approval(appt['id'], 'NOC', noc_action, user['username'])
                        st.success(f"✅ NOC updated to {noc_action}")
                        st.rerun()
    else:
        st.success("✅ No pending approvals!")


def show_activity_logs():
    st.header("📜 Activity Logs")
    if st.session_state.activity_log:
        log_df = pd.DataFrame(st.session_state.activity_log)
        log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
        log_df = log_df.sort_values('timestamp', ascending=False)

        def extract_isa(details):
            if 'ISA:' in str(details):
                try:
                    return str(details).split('ISA:')[1].split(',')[0].strip()
                except:
                    return ''
            return ''

        log_df['ID (ISA)'] = log_df['details'].apply(extract_isa)
        cols = ['ID (ISA)', 'timestamp', 'user', 'action', 'details']
        st.dataframe(log_df[cols], use_container_width=True, height=500)

        csv = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Activity Logs", csv,
                           f"activity_logs_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("📭 No activity logs yet")
