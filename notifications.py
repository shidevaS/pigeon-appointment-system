import hashlib
import streamlit as st
from datetime import datetime


def log_activity(user: str, action: str, details: str):
    st.session_state.db.log_activity(user, action, details)
    st.session_state.activity_log.append({
        'timestamp': datetime.now(),
        'user': user,
        'action': action,
        'details': details
    })


def add_notification(message: str, severity: str = "info", vendor_name: str = None):
    notif_id = hashlib.md5(f"{datetime.now()}{message}".encode()).hexdigest()[:8]
    st.session_state.db.add_notification(notif_id, message, severity, vendor_name=vendor_name)
    notification = {
        'timestamp': datetime.now(),
        'message': message,
        'severity': severity,
        'id': notif_id,
        'vendor_name': vendor_name
    }
    st.session_state.notifications.insert(0, notification)
    if len(st.session_state.notifications) > 50:
        st.session_state.notifications.pop()


def broadcast_notification(message: str, severity: str = "info", vendor_name: str = None):
    add_notification(f"📢 {message}", severity, vendor_name=vendor_name)
