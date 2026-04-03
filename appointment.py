import hashlib
import numpy as np
import streamlit as st
from datetime import datetime
from notifications import broadcast_notification, log_activity


class CategoryAppointment:
    @staticmethod
    def create_appointment(vendor_code, vendor_name, fc, category, units, cartons,
                           appt_date, prepone_date, lead_time, remarks, isa=None, ape_rank=None, sml_mix=None):
        appointment = {
            'id': hashlib.md5(f"{datetime.now()}{vendor_code}{fc}".encode()).hexdigest()[:10],
            'IOG': f"IOG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{np.random.randint(1000, 9999)}",
            'vendor_code': vendor_code,
            'vendor_name': vendor_name,
            'fc': fc,
            'category': category,
            'ISA': isa if isa else '',
            'ape_rank': ape_rank if ape_rank else '',
            'units': units,
            'cartons': cartons,
            'sml_mix': sml_mix if sml_mix else 'N/A',
            'appt_date': appt_date,
            'prepone_date': prepone_date,
            'lead_time': lead_time,
            'ibsc_remarks': remarks,
            'status': 'Pending',
            'ibsc_approval': 'Pending',
            'noc_approval': 'Pending',
            'created_at': datetime.now(),
            'created_by': vendor_name
        }
        success = st.session_state.db.create_appointment(appointment)
        if success:
            st.session_state.category_appointments.append(appointment)
            broadcast_notification(
                f"New Appointment: {vendor_name} - {category} at {fc} ({units} units) - ISA: {isa}",
                "info", vendor_name=vendor_name
            )
            log_activity(vendor_name, 'appointment_created', f"ISA: {appointment['ISA']}")
            return appointment
        return None

    @staticmethod
    def update_approval(appt_id, approval_type, status, approver,
                        revised_date=None, revised_time=None, noc_remarks=None, ibsc_team_remarks=None):
        success = st.session_state.db.update_approval(
            appt_id, approval_type, status, approver, revised_date, revised_time, noc_remarks, ibsc_team_remarks
        )
        if success:
            for appt in st.session_state.category_appointments:
                if appt['id'] == appt_id:
                    if approval_type == 'IBSC':
                        appt['ibsc_approval'] = status
                        appt['ibsc_approver'] = approver
                        appt['ibsc_approved_at'] = datetime.now()
                        if ibsc_team_remarks:
                            appt['ibsc_team_remarks'] = ibsc_team_remarks
                    elif approval_type == 'NOC':
                        appt['noc_approval'] = status
                        appt['noc_approver'] = approver
                        appt['noc_approved_at'] = datetime.now()
                        if revised_date:
                            appt['noc_revised_date'] = revised_date
                        if noc_remarks:
                            appt['noc_remarks'] = noc_remarks
                    if appt['ibsc_approval'] == 'Approved' and appt['noc_approval'] == 'Approved':
                        appt['status'] = 'Executed'
                        appt['execution_comment'] = 'Scheduling updated and executed by NOC team'
                    elif appt['ibsc_approval'] == 'Rejected' or appt['noc_approval'] == 'Rejected':
                        appt['status'] = 'Rejected'
                    elif appt['ibsc_approval'] == 'On Hold' or appt['noc_approval'] == 'On Hold':
                        appt['status'] = 'On Hold'
                    broadcast_notification(
                        f"{approval_type} {status}: ISA {appt['ISA']} - {appt['vendor_name']}",
                        "success" if status == "Approved" else "warning",
                        vendor_name=appt['vendor_name']
                    )
                    log_activity(approver, f'{approval_type}_approval', f"ISA: {appt['ISA']}, Status: {status}")
                    break
        return success

    @staticmethod
    def get_vendor_appointments(vendor_name):
        db_appointments = st.session_state.db.get_vendor_appointments(vendor_name)
        st.session_state.category_appointments = st.session_state.db.get_all_appointments()
        return db_appointments

    @staticmethod
    def get_pending_approvals():
        db_pending = st.session_state.db.get_pending_approvals()
        st.session_state.category_appointments = st.session_state.db.get_all_appointments()
        return db_pending
