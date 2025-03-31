import sqlite3
from config import DB_PATH
from db import queries


import sqlite3
from config import DB_PATH
from db import queries

def get_bought_items_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items WHERE completed = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()


def get_items(filter_type="all"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if filter_type == 'bought':
        cursor.execute(queries.SELECT_bought)
    elif filter_type == "not_bought":
        cursor.execute(queries.SELECT_not_bought)
    else:
        cursor.execute(queries.SELECT_ITEMS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_item_db(item):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_ITEM, (item,))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id


def update_item_db(item_id, new_item=None, bought=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_item is not None:
        cursor.execute("UPDATE items SET task = ? WHERE id = ?", (new_item, item_id))
    if  bought is not None:
        cursor.execute("UPDATE items SET completed = ? WHERE id = ?", (bought, item_id))

    conn.commit()
    conn.close()

def delete_item_db(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_ITEM, (item_id,))
    conn.commit()
    conn.close()
