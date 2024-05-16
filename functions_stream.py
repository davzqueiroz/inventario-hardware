import sqlite3


def connection():
    conn = sqlite3.connect('bank_rad')
    return conn

