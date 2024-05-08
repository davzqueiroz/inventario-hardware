import sqlite3


def connection(bank_rad):
    conn = sqlite3.connect(bank_rad)
    return conn
