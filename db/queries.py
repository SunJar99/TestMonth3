CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

SELECT_ITEMS = "SELECT id, item, completed FROM items ORDER BY id DESC"

INSERT_ITEM = "INSERT INTO items (item) VALUES (?)"


UPDATE_ITEM = """
    UPDATE items
    SET task = COALESCE(?, item),
        completed = COALESCE(?, completed)
    WHERE id = ?
"""


DELETE_ITEM = "DELETE FROM items WHERE id = ?"

SELECT_bought = "SELECT id, item, completed FROM items WHERE completed = 1 ORDER BY id DESC"

SELECT_not_bought = "SELECT id, item, completed FROM items WHERE completed = 0 ORDER BY id DESC"