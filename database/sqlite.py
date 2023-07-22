import sqlite3
from config import DB_NAME


def create_table(query):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


def insert_data(data,query):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()
    finally:
        conn.close()

