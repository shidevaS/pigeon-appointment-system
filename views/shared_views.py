import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def show_all_appointments_view():
    st.header("📊 All Appointments")
    st.session_state.category_appointments = st.session_state.db.get_all_appointments()

    if st.session_state.category_appointments:
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            status_filter = st.multiselect("Filter by Status",
                ['Pending', 'On Hold', 'Executed', 'Rejected'],
                default=['Pending', 'On Hold', 'Executed'])
        with filter_col2:
            all_vendors = list(set([a['vendor_name'] for a in st.session_state.category_appointments]))
            vendor_filter = st.multiselect("Filter by Vendor", all_vendors, default=all_vendors)
        with filter_col3:
            category_filter = st.multiselect("Filter by Category",
                ['GL', 'PL', 'FC'], default=['GL', 'PL', 'FC'])

        filtered_appts = [
            a for a in st.session_state.category_appointments
            if a['status'] in status_filter
            and a['vendor_name'] in vendor_filter
            and a['category'] in category_filter
        ]
        st.metric("Filtered Appointments", len(filtered_appts))

        if filtered_appts:
            appt_df = pd.DataFrame(filtered_appts)
            display_cols = ['ISA', 'vendor_name', 'fc', 'category', 'units', 'cartons',
                            'appt_date', 'prepone_date', 'ibsc_approval', 'noc_approval', 'status']
            missing_cols = [col for col in display_cols if col not in appt_df.columns]
            if missing_cols:
                st.error(f"Missing columns: {missing_cols}")
            else:
                st.dataframe(appt_df[display_cols], use_container_width=True, height=400)
                csv = appt_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Appointments", csv,
                                   f"appointments_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.info("No appointments match the current filters")
    else:
        st.info("📭 No appointments yet")


def show_dashboard_view():
    st.header("📈 Dashboard & Analytics")
    st.session_state.category_appointments = st.session_state.db.get_all_appointments()

    user = st.session_state.user_session
    if user['role'] == 'seller':
        filtered_appts = [a for a in st.session_state.category_appointments
                          if a['vendor_name'] == user['vendor_name']]
    else:
        filtered_appts = st.session_state.category_appointments

    if filtered_appts:
        appt_df = pd.DataFrame(filtered_appts)

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi1.metric("Total", len(appt_df))
        kpi2.metric("Pending", len(appt_df[appt_df['status'] == 'Pending']))
        kpi3.metric("On Hold", len(appt_df[appt_df['status'] == 'On Hold']))
        kpi4.metric("Executed", len(appt_df[appt_df['status'] == 'Executed']))
        kpi5.metric("Rejected", len(appt_df[appt_df['status'] == 'Rejected']))
        st.markdown("---")

        chart_row1_col1, chart_row1_col2 = st.columns(2)
        with chart_row1_col1:
            status_counts = appt_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig = px.pie(status_counts, values='Count', names='Status',
                         title="Appointment Status Distribution",
                         color='Status', color_discrete_map={
                             'Pending': '#ff9800', 'On Hold': '#2196F3',
                             'Executed': '#4caf50', 'Rejected': '#f44336'})
            st.plotly_chart(fig, use_container_width=True)
        with chart_row1_col2:
            vendor_counts = appt_df['vendor_name'].value_counts().reset_index()
            vendor_counts.columns = ['Vendor', 'Count']
            fig2 = px.bar(vendor_counts, x='Vendor', y='Count',
                          title="Appointments by Vendor", color='Vendor')
            st.plotly_chart(fig2, use_container_width=True)

        chart_row2_col1, chart_row2_col2 = st.columns(2)
        with chart_row2_col1:
            cat_counts = appt_df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig3 = px.bar(cat_counts, x='Category', y='Count',
                          title="Appointments by Category", color='Category')
            st.plotly_chart(fig3, use_container_width=True)
        with chart_row2_col2:
            fc_counts = appt_df['fc'].value_counts().head(10).reset_index()
            fc_counts.columns = ['FC Node', 'Count']
            fig4 = px.bar(fc_counts, x='FC Node', y='Count', title="Top 10 FC Nodes",
                          color='Count', color_continuous_scale='Blues')
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Approval Statistics")
        approval_col1, approval_col2 = st.columns(2)
        with approval_col1:
            ibsc_counts = appt_df['ibsc_approval'].value_counts().reset_index()
            ibsc_counts.columns = ['IBSC Status', 'Count']
            fig5 = px.pie(ibsc_counts, values='Count', names='IBSC Status', title="IBSC Approval Status")
            st.plotly_chart(fig5, use_container_width=True)
        with approval_col2:
            noc_counts = appt_df['noc_approval'].value_counts().reset_index()
            noc_counts.columns = ['NOC Status', 'Count']
            fig6 = px.pie(noc_counts, values='Count', names='NOC Status', title="NOC Approval Status")
            st.plotly_chart(fig6, use_container_width=True)
    else:
        st.info("📊 No data available yet")
