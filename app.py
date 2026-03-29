import streamlit as st
from datetime import datetime
from eagle_database import EagleDatabase
from notifications import log_activity, add_notification

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EAGLE - P3P Interaction Gateway",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🦅"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
.main { background-color: #f0f2f6; }
.eagle-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 20px; border-radius: 10px;
    margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.eagle-tagline { font-size: 14px; font-style: italic; color: #e0e0e0; margin-top: 5px; }
.appointment-card {
    background: white; padding: 20px; border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;
}
.status-pending { border-left: 5px solid #ff9800; }
.status-approved { border-left: 5px solid #4caf50; }
.status-rejected { border-left: 5px solid #f44336; }
.status-onhold { border-left: 5px solid #2196F3; }
.status-executed { border-left: 5px solid #00bcd4; }
.info-box {
    background: #e8eaf6; padding: 15px; border-radius: 8px;
    border-left: 4px solid #5c6bc0; margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'user_session' not in st.session_state:
    st.session_state.user_session = None
if 'db' not in st.session_state:
    st.session_state.db = EagleDatabase()
if 'category_appointments' not in st.session_state:
    st.session_state.category_appointments = st.session_state.db.get_all_appointments()
if 'notifications' not in st.session_state:
    st.session_state.notifications = st.session_state.db.get_notifications(50)
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = st.session_state.db.get_activity_logs(100)


# --- AUTH ---
class AuthSystem:
    USERS = {
        'admin':     {'password': 'admin123',  'role': 'admin',  'name': 'SIMS Admin',  'email': 'admin@company.com'},
        'rk':        {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'RK',              'vendor_id': 109,     'email': 'rk@vendor.com'},
        'kkoc':      {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'KKOC',            'vendor_id': 104,     'email': 'kkoc@vendor.com'},
        'etrade':    {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'Etrade',          'vendor_id': 107,     'email': 'etrade@vendor.com'},
        'cocoblu':   {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'CoCoblu',         'vendor_id': 108,     'email': 'cocoblu@vendor.com'},
        'retailez':  {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'Retail_Ez',       'vendor_id': 113,     'email': 'retailez@vendor.com'},
        'clicktech': {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'Clicktech_RFul1', 'vendor_id': 7870951, 'email': 'clicktech@vendor.com'},
        'ohl':       {'password': 'vendor123', 'role': 'seller', 'vendor_name': 'OHL',             'vendor_id': 110,     'email': 'ohl@vendor.com'},
        'ibsc':      {'password': 'ibsc123',   'role': 'ibsc',   'name': 'IBSC Team', 'team': 'Inbound Supply Chain',      'email': 'ibsc@company.com'},
        'noc':       {'password': 'noc123',    'role': 'noc',    'name': 'NOC Team',  'team': 'Network Operations Center', 'email': 'noc@company.com'},
    }

    @staticmethod
    def login(username, password):
        user = AuthSystem.USERS.get(username.lower())
        if user and user['password'] == password:
            st.session_state.user_session = {
                'username': username, 'role': user['role'],
                'vendor_name': user.get('vendor_name'), 'vendor_id': user.get('vendor_id'),
                'name': user.get('name', username), 'team': user.get('team', ''),
                'email': user.get('email', ''), 'login_time': datetime.now()
            }
            log_activity(username, 'login', f'{user["role"]} logged in')
            add_notification(f"{username} joined the portal", "info")
            return True
        return False

    @staticmethod
    def logout():
        if st.session_state.user_session:
            log_activity(st.session_state.user_session['username'], 'logout', 'User logged out')
            st.session_state.user_session = None

    @staticmethod
    def is_authenticated():
        return st.session_state.user_session is not None


# --- LOGIN PAGE ---
def show_login_page():
    st.markdown("""
    <div class="eagle-header">
        <h1>🦅 EAGLE</h1>
        <h3>P3P Interaction Gateway to Engage Online</h3>
        <p class="eagle-tagline">AI-powered communication platform connecting P3P sellers, SIMS, and Amazon teams</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>About EAGLE:</strong><br>
        EAGLE eliminates communication silos and reduces manual coordination overhead by providing real-time visibility
        across all stakeholders — empowering unified visibility and effective, faster close-looping.
    </div>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
            <h3 style="color: white; text-align: center;">🔐 Secure Access Portal</h3>
            <p style="color: #e0e0e0; text-align: center; font-size: 14px;">Category Appointment Management</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔓 Login", type="primary", use_container_width=True):
                if AuthSystem.login(username, password):
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        with c2:
            if st.button("🔄 Reset", use_container_width=True):
                st.rerun()
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 12px; margin-top: 16px;">
            <p>🦅 EAGLE — Powered by Amazon SIMS</p>
        </div>
        """, unsafe_allow_html=True)


# --- MAIN APP ---
def show_main_app():
    from views.seller_views import show_seller_views
    from views.ibsc_views import show_ibsc_views
    from views.noc_views import show_noc_views
    from views.admin_views import show_admin_views

    user = st.session_state.user_session

    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("""
        <div class="eagle-header">
            <h2>🦅 EAGLE - Category Appointment Management</h2>
            <p class="eagle-tagline">P3P Interaction Gateway | Unified visibility, effective & faster close-looping</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"👤 {user['name']} ({user['role'].upper()}) | 🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col_h2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            AuthSystem.logout()
            st.rerun()

    st.markdown("---")

    # Sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h2>🦅 EAGLE</h2>
        <p style="font-size: 12px; color: #666;">P3P Interaction Gateway</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.title("🎛️ Navigation")

    menus = {
        'seller': ["📝 Create Appointment", "📊 My Appointments", "📈 Dashboard"],
        'ibsc':   ["✅ IBSC Approvals", "🔄 Slot Override Requests", "📊 All Appointments", "📈 Dashboard"],
        'noc':    ["✅ NOC Approvals", "📊 All Appointments", "📈 Dashboard"],
        'admin':  ["📊 All Appointments", "✅ Approval Management", "📈 Dashboard", "📜 Activity Logs"],
    }
    app_mode = st.sidebar.radio("📍 Menu", menus[user['role']])

    # Notifications
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔔 Recent Notifications")
    notifs = (st.session_state.db.get_notifications(20, vendor_name=user['vendor_name'])
              if user['role'] == 'seller'
              else st.session_state.db.get_notifications(20))
    if notifs:
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "🚨", "success": "✅"}
        for n in notifs[:5]:
            st.sidebar.markdown(f"{icons.get(n['severity'], 'ℹ️')} {n['message']}")
            st.sidebar.caption(n['timestamp'].strftime('%H:%M:%S'))
    else:
        st.sidebar.info("No notifications")

    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Quick Stats")
    appts = ([a for a in st.session_state.category_appointments if a['vendor_name'] == user['vendor_name']]
             if user['role'] == 'seller' else st.session_state.category_appointments)
    st.sidebar.metric("Total", len(appts))
    st.sidebar.metric("Pending",  len([a for a in appts if a['status'] == 'Pending']))
    st.sidebar.metric("Executed", len([a for a in appts if a['status'] == 'Executed']))
    st.sidebar.metric("Hold",     len([a for a in appts if a['status'] == 'On Hold']))
    st.sidebar.metric("Rejected", len([a for a in appts if a['status'] == 'Rejected']))

    # Route
    role = user['role']
    if role == 'seller':
        show_seller_views(user, app_mode)
    elif role == 'ibsc':
        show_ibsc_views(user, app_mode)
    elif role == 'noc':
        show_noc_views(user, app_mode)
    elif role == 'admin':
        show_admin_views(user, app_mode)


# --- ENTRY POINT ---
if not AuthSystem.is_authenticated():
    show_login_page()
else:
    show_main_app()
