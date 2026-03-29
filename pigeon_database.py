import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any


DB_PATH = "pigeon.db"


def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


class PigeonDatabase:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        with _get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id TEXT PRIMARY KEY,
                    iog TEXT,
                    vendor_code TEXT,
                    vendor_name TEXT,
                    fc TEXT,
                    category TEXT,
                    isa TEXT,
                    units INTEGER,
                    cartons INTEGER,
                    sml_mix TEXT,
                    appt_date TEXT,
                    prepone_date TEXT,
                    lead_time INTEGER,
                    ibsc_remarks TEXT,
                    status TEXT DEFAULT 'Pending',
                    ibsc_approval TEXT DEFAULT 'Pending',
                    noc_approval TEXT DEFAULT 'Pending',
                    ibsc_approver TEXT,
                    ibsc_approved_at TEXT,
                    ibsc_team_remarks TEXT,
                    noc_approver TEXT,
                    noc_approved_at TEXT,
                    noc_revised_date TEXT,
                    noc_remarks TEXT,
                    execution_comment TEXT,
                    slot_override_requested INTEGER DEFAULT 0,
                    slot_override_reason TEXT,
                    slot_override_status TEXT,
                    slot_override_requested_at TEXT,
                    slot_override_ibsc_response TEXT,
                    created_at TEXT,
                    created_by TEXT
                );

                CREATE TABLE IF NOT EXISTS notifications (
                    id TEXT PRIMARY KEY,
                    message TEXT,
                    severity TEXT DEFAULT 'info',
                    vendor_name TEXT,
                    timestamp TEXT
                );

                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    action TEXT,
                    details TEXT,
                    timestamp TEXT
                );
            """)

    def _row_to_appt(self, row) -> Dict[str, Any]:
        d = dict(row)
        for date_field in ['appt_date', 'prepone_date', 'noc_revised_date']:
            if d.get(date_field):
                try:
                    d[date_field] = datetime.strptime(d[date_field], '%Y-%m-%d').date()
                except:
                    pass
        for dt_field in ['created_at', 'ibsc_approved_at', 'noc_approved_at', 'slot_override_requested_at']:
            if d.get(dt_field):
                try:
                    d[dt_field] = datetime.fromisoformat(d[dt_field])
                except:
                    pass
        d['slot_override_requested'] = bool(d.get('slot_override_requested', 0))
        # Normalize keys
        d['IOG'] = d.pop('iog', '')
        d['ISA'] = d.pop('isa', '')
        return d

    def create_appointment(self, appt: Dict[str, Any]) -> bool:
        try:
            with _get_conn() as conn:
                conn.execute("""
                    INSERT INTO appointments (
                        id, iog, vendor_code, vendor_name, fc, category, isa, units, cartons,
                        sml_mix, appt_date, prepone_date, lead_time, ibsc_remarks,
                        status, ibsc_approval, noc_approval, created_at, created_by
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    appt['id'], appt['IOG'], str(appt['vendor_code']), appt['vendor_name'],
                    appt['fc'], appt['category'], appt['ISA'], appt['units'], appt['cartons'],
                    appt.get('sml_mix', 'N/A'),
                    str(appt['appt_date']), str(appt['prepone_date']),
                    appt['lead_time'], appt.get('ibsc_remarks', ''),
                    appt.get('status', 'Pending'),
                    appt.get('ibsc_approval', 'Pending'),
                    appt.get('noc_approval', 'Pending'),
                    appt['created_at'].isoformat(),
                    appt['created_by']
                ))
            return True
        except Exception as e:
            print(f"[DB] create_appointment error: {e}")
            return False

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            rows = conn.execute("SELECT * FROM appointments ORDER BY created_at DESC").fetchall()
        return [self._row_to_appt(r) for r in rows]

    def get_vendor_appointments(self, vendor_name: str) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE vendor_name=? ORDER BY created_at DESC",
                (vendor_name,)
            ).fetchall()
        return [self._row_to_appt(r) for r in rows]

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE ibsc_approval IN ('Pending','On Hold') OR noc_approval IN ('Pending','On Hold') ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_appt(r) for r in rows]

    def update_approval(self, appt_id: str, approval_type: str, status: str, approver: str,
                        revised_date=None, noc_remarks: str = None, ibsc_team_remarks: str = None) -> bool:
        try:
            with _get_conn() as conn:
                now = datetime.now().isoformat()
                if approval_type == 'IBSC':
                    conn.execute("""
                        UPDATE appointments SET ibsc_approval=?, ibsc_approver=?, ibsc_approved_at=?,
                        ibsc_team_remarks=COALESCE(?, ibsc_team_remarks) WHERE id=?
                    """, (status, approver, now, ibsc_team_remarks, appt_id))
                elif approval_type == 'NOC':
                    conn.execute("""
                        UPDATE appointments SET noc_approval=?, noc_approver=?, noc_approved_at=?,
                        noc_revised_date=COALESCE(?, noc_revised_date),
                        noc_remarks=COALESCE(?, noc_remarks) WHERE id=?
                    """, (status, approver, now,
                          str(revised_date) if revised_date else None,
                          noc_remarks, appt_id))

                # Recalculate overall status
                row = conn.execute(
                    "SELECT ibsc_approval, noc_approval FROM appointments WHERE id=?", (appt_id,)
                ).fetchone()
                if row:
                    ibsc, noc = row['ibsc_approval'], row['noc_approval']
                    if ibsc == 'Approved' and noc == 'Approved':
                        new_status = 'Executed'
                        conn.execute(
                            "UPDATE appointments SET status=?, execution_comment=? WHERE id=?",
                            (new_status, 'Scheduling updated and executed by NOC team', appt_id)
                        )
                    elif ibsc == 'Rejected' or noc == 'Rejected':
                        conn.execute("UPDATE appointments SET status='Rejected' WHERE id=?", (appt_id,))
                    elif ibsc == 'On Hold' or noc == 'On Hold':
                        conn.execute("UPDATE appointments SET status='On Hold' WHERE id=?", (appt_id,))
            return True
        except Exception as e:
            print(f"[DB] update_approval error: {e}")
            return False

    def request_slot_override(self, appt_id: str, reason: str, requested_by: str) -> bool:
        try:
            with _get_conn() as conn:
                conn.execute("""
                    UPDATE appointments SET slot_override_requested=1, slot_override_reason=?,
                    slot_override_status='Pending', slot_override_requested_at=? WHERE id=?
                """, (reason, datetime.now().isoformat(), appt_id))
            return True
        except Exception as e:
            print(f"[DB] request_slot_override error: {e}")
            return False

    def respond_slot_override(self, appt_id: str, status: str, responder: str, response: str = None) -> bool:
        try:
            with _get_conn() as conn:
                conn.execute("""
                    UPDATE appointments SET slot_override_status=?,
                    slot_override_ibsc_response=COALESCE(?, slot_override_ibsc_response) WHERE id=?
                """, (status, response, appt_id))
            return True
        except Exception as e:
            print(f"[DB] respond_slot_override error: {e}")
            return False

    def get_slot_override_requests(self) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE slot_override_requested=1 AND slot_override_status='Pending'"
            ).fetchall()
        return [self._row_to_appt(r) for r in rows]

    def add_notification(self, notif_id: str, message: str, severity: str = 'info',
                         vendor_name: str = None) -> bool:
        try:
            with _get_conn() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO notifications (id, message, severity, vendor_name, timestamp) VALUES (?,?,?,?,?)",
                    (notif_id, message, severity, vendor_name, datetime.now().isoformat())
                )
            return True
        except Exception as e:
            print(f"[DB] add_notification error: {e}")
            return False

    def get_notifications(self, limit: int = 20, vendor_name: str = None) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            if vendor_name:
                rows = conn.execute(
                    "SELECT * FROM notifications WHERE vendor_name=? OR vendor_name IS NULL ORDER BY timestamp DESC LIMIT ?",
                    (vendor_name, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM notifications ORDER BY timestamp DESC LIMIT ?", (limit,)
                ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d['timestamp'] = datetime.fromisoformat(d['timestamp'])
            except:
                d['timestamp'] = datetime.now()
            result.append(d)
        return result

    def log_activity(self, user: str, action: str, details: str) -> bool:
        try:
            with _get_conn() as conn:
                conn.execute(
                    "INSERT INTO activity_logs (user, action, details, timestamp) VALUES (?,?,?,?)",
                    (user, action, details, datetime.now().isoformat())
                )
            return True
        except Exception as e:
            print(f"[DB] log_activity error: {e}")
            return False

    def get_activity_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d['timestamp'] = datetime.fromisoformat(d['timestamp'])
            except:
                d['timestamp'] = datetime.now()
            result.append(d)
        return result
