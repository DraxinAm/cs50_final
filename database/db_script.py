import sqlite3

SQL_COMMAND = """
SELECT * FROM users
"""
conn = sqlite3.connect('recipes.db')
print(conn.execute(SQL_COMMAND).fetchall())
conn.close()