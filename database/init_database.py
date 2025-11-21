import sqlite3

conn = sqlite3.connect('recipes.db')
with open('schema.sql', 'r') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print("Database initialized successfully!")