"""정적 분석 샘플: SQL Injection (CWE-89)."""

import sqlite3


def login(conn: sqlite3.Connection, user: str, pw: str):
    cur = conn.cursor()
    query = "SELECT id FROM users WHERE name='%s' AND password='%s'" % (user, pw)
    cur.execute(query)
    return cur.fetchone()


def search_posts(conn: sqlite3.Connection, keyword: str):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{keyword}%'")
    return cur.fetchall()


def delete_user(conn: sqlite3.Connection, uid: str):
    conn.executescript("DELETE FROM users WHERE id = " + uid)
