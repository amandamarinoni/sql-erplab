from pathlib import Path
import sqlite3
from src.build_db import build_db

def test_db_and_queries():
    db_path = Path("erp.db")
    if db_path.exists(): db_path.unlink()
    build_db(db_path)
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM Customers"); assert cur.fetchone()[0] >= 1
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='OrderItems'"); assert cur.fetchone() is not None
    con.close()
