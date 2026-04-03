import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from appointment import CategoryAppointment


def show_seller_views(user, app_mode):
    vendor_name = user['vendor_name']
    vendor_id = user['vendor_id']

    if app_mode == "📝 Create Appointment":
        show_create_appointment(vendor_name, vendor_id)
    elif app_mode == "📊 My Appointments":
        show_my_appointments(vendor_name)
    elif app_mode == "📈 Dashboard":
        show_seller_dashboard(vendor_name)


def show_create_appointment(vendor_name, vendor_id):
    st.header(f"📝 Create New Appointment Pull Request - {vendor_name}")
    with st.form("appointment_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            fc_node = st.selectbox("FC Node *", [
                'BLR8', 'BLR7', 'ISK3', 'BOM5', 'DEL4', 'DEL5', 'DED5', 'HYD8',
                'MAA4', 'BOM7', 'DED4', 'CJB1', 'PNQ3', 'DED3', 'HYD3', 'AMD2',
                'BLR4', 'CCX2', 'CCX1', 'LKO1', 'PAX1', 'ATX1', 'BBX1', 'HDX1',
                'LDX1', 'IDX2', 'CCX4'
            ])
            category = st.selectbox("Category *", ['GL', 'PL', 'FC'])
            isa = st.text_input("ISA ID * (Numbers only)", value="", placeholder="e.g., 123456")
            ape_rank = st.selectbox("APE Rank *", ['A+', 'A', 'B', 'C', 'D'])
        with col2:
            units = st.number_input("Units *", min_value=1, value=1000, step=100)
            cartons = st.number_input("Cartons *", min_value=1, value=50, step=10)
            sml_mix = st.text_input("SML Mix", placeholder="e.g., S:30%, M:50%, L:20%")
        with col3:
            current_scheduled_date = st.date_input("Current Scheduled Date *", datetime.now() + timedelta(days=3))
            requested_pull_date = st.date_input("Requested Pull Date *", datetime.now() + timedelta(days=1))
            lead_time_hr = st.number_input("Lead Time (hours) *", min_value=1, value=48, step=1)
        remarks = st.text_area("Remarks", placeholder="Enter any special instructions or comments...")
        submitted = st.form_submit_button("📤 Submit Appointment Request", type="primary", use_container_width=True)

        if submitted:
            if not isa or not isa.strip():
                st.error("❌ ISA ID is required!")
            elif not isa.strip().isdigit():
                st.error("❌ ISA ID must contain numbers only!")
            else:
                appointment = CategoryAppointment.create_appointment(
                    vendor_id, vendor_name, fc_node, category, units, cartons,
                    current_scheduled_date, requested_pull_date, lead_time_hr,
                    remarks, isa.strip(), ape_rank, sml_mix
                )
                if appointment:
                    st.success(f"✅ Appointment created! ISA ID: {appointment['ISA']}")
                    st.info("📨 Request sent to IBSC and NOC teams for approval")
                    st.balloons()
                else:
                    st.error("❌ Error creating appointment. Please try again.")


def show_my_appointments(vendor_name):
    st.header(f"📊 My Appointment Requests - {vendor_name}")
    vendor_appointments = st.session_state.db.get_vendor_appointments(vendor_name)

    if vendor_appointments:
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            status_filter = st.multiselect("Filter by Status",
                ['Pending', 'On Hold', 'Executed', 'Rejected'],
                default=['Pending', 'On Hold', 'Executed'])
        with filter_col2:
            category_filter = st.multiselect("Filter by Category",
                ['GL', 'PL', 'FC'], default=['GL', 'PL', 'FC'])

        filtered_appts = [a for a in vendor_appointments
                          if a['status'] in status_filter and a['category'] in category_filter]
        st.metric("Total Appointments", len(filtered_appts))

        for appt in reversed(filtered_appts):
            status_class = {
                'Pending': 'status-pending', 'On Hold': 'status-onhold',
                'Executed': 'status-executed', 'Approved': 'status-approved',
                'Rejected': 'status-rejected'
            }.get(appt['status'], '')

            with st.container():
                st.markdown(f"""
                <div class="appointment-card {status_class}">
                    <h4>ISA ID: {appt['ISA']} | Status: {appt['status']}</h4>
                </div>
                """, unsafe_allow_html=True)

                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.write(f"**FC Node:** {appt['fc']}")
                    st.write(f"**Category:** {appt['category']}")
                    st.write(f"**ISA:** {appt['ISA']}")
                with col_info2:
                    st.write(f"**Units:** {appt['units']:,}")
                    st.write(f"**Cartons:** {appt['cartons']}")
                    st.write(f"**SML Mix:** {appt.get('sml_mix', 'N/A')}")
                with col_info3:
                    st.write(f"**Scheduled Date:** {appt['appt_date']}")
                    st.write(f"**Requested Date:** {appt['prepone_date']}")
                    st.write(f"**Lead Time:** {appt['lead_time']} hr")
                    st.write(f"**Remarks:** {appt['ibsc_remarks']}")

                if appt.get('ibsc_team_remarks'):
                    st.info(f"💬 **IBSC Team Remarks:** {appt['ibsc_team_remarks']}")

                approval_col1, approval_col2 = st.columns(2)
                with approval_col1:
                    ibsc_color = {'Pending': '🟡', 'Approved': '✅', 'Rejected': '❌', 'On Hold': '⏸️'}.get(appt['ibsc_approval'], '⚪')
                    st.write(f"**IBSC Approval:** {ibsc_color} {appt['ibsc_approval']}")
                with approval_col2:
                    noc_color = {'Pending': '🟡', 'Approved': '✅', 'Rejected': '❌', 'On Hold': '⏸️'}.get(appt['noc_approval'], '⚪')
                    st.write(f"**NOC Approval:** {noc_color} {appt['noc_approval']}")
                    if appt.get('noc_revised_date'):
                        st.info(f"📅 NOC Revised Date: {appt['noc_revised_date']}")
                    if appt.get('noc_remarks'):
                        st.info(f"💬 **NOC Remarks:** {appt['noc_remarks']}")

                if appt['status'] == 'Executed':
                    st.success(f"✅ {appt.get('execution_comment', 'Executed successfully')}")
                st.markdown("---")
    else:
        st.info("📭 No appointments yet. Create your first appointment request!")


def show_seller_dashboard(vendor_name):
    st.header(f"📈 Dashboard - {vendor_name}")
    vendor_appointments = st.session_state.db.get_vendor_appointments(vendor_name)

    if vendor_appointments:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Requests", len(vendor_appointments))
        kpi2.metric("Pending", len([a for a in vendor_appointments if a['status'] == 'Pending']))
        kpi3.metric("Executed", len([a for a in vendor_appointments if a['status'] == 'Executed']))
        kpi4.metric("Rejected", len([a for a in vendor_appointments if a['status'] == 'Rejected']))
        st.markdown("---")

        chart_col1, chart_col2 = st.columns(2)
        appt_df = pd.DataFrame(vendor_appointments)
        with chart_col1:
            status_counts = appt_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig = px.pie(status_counts, values='Count', names='Status', title="Status Distribution",
                         color='Status', color_discrete_map={
                             'Pending': '#ff9800', 'On Hold': '#2196F3',
                             'Executed': '#4caf50', 'Rejected': '#f44336'})
            st.plotly_chart(fig, use_container_width=True)
        with chart_col2:
            cat_counts = appt_df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig2 = px.bar(cat_counts, x='Category', y='Count', title="Appointments by Category", color='Category')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📊 No data available yet. Create appointments to see analytics.")
