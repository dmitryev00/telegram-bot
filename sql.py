import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta


def set_data(lat, lon, date, username):
    with get_db() as conn:
        delete_expired_data()
        cursor = conn.cursor()
        data = (lat, lon, date, username)
        cursor.execute('INSERT INTO markers (lat, lon, date, username) VALUES (?, ?, ?, ?)', data)
        conn.commit()


def delete_expired_data():
    with get_db() as conn:
        cursor = conn.cursor()
        threshold = datetime.now() - timedelta(hours=3)
        cursor.execute('DELETE FROM markers WHERE date < ?', (threshold.strftime('%d.%m.%Y %H:%M'),))
        conn.commit()


def get_data():
    with get_db() as conn:
        delete_expired_data()
        points = conn.execute("SELECT lat, lon FROM markers").fetchall()
    return points


@contextmanager
def get_db():
    conn = sqlite3.connect("locations.db")
    try:
        yield conn
    finally:
        conn.close()
