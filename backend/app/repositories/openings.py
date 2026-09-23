import sqlite3

def _cols(conn):
    return {r[1] for r in conn.execute("PRAGMA table_info(openings)").fetchall()}

def ensure_schema(conn):
    """老库补列：开洞留边宽度，缺省 0（等同改造前）。"""
    if "trim" not in _cols(conn):
        conn.execute("ALTER TABLE openings ADD COLUMN trim REAL NOT NULL DEFAULT 0")
        conn.commit()

def for_room(conn, room_id):
    return [dict(r) for r in conn.execute("SELECT * FROM openings WHERE room_id=?", (room_id,)).fetchall()]

def set_trim(conn, opening_id, trim):
    cur = conn.execute("UPDATE openings SET trim=? WHERE id=?", (float(trim), opening_id))
    conn.commit()
    return cur.rowcount

def get(conn, opening_id):
    row = conn.execute("SELECT * FROM openings WHERE id=?", (opening_id,)).fetchone()
    return dict(row) if row else None
