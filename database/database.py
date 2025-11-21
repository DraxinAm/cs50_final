# import sqlite3
# from login import problem

# class Database:
#     def __init__(self, db_file="database/recipes.db"):
#         self.db_file = db_file

#     def execute(self, query, params):
#         self.connection = sqlite3.connect("database/recipes.db")
#         self.cursor = self.connection.cursor()

#         try:
#             self.cursor.execute(query, params)
#             self.connection.commit()
#         except Exception:
#             print("Query failed")
#             self.connection.close()
        
#         print("Query successfully called.")
#         self.connection.close()

import sqlite3

class Database:
    def __init__(self, db_file="database/recipes.db"):
        self.db_file = db_file

    def insert_username_and_password(self, username, password):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

    def get_user_by_username(self, username):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = dict(cursor.fetchone())
        connection.close()
        return result
    
    def connection_and_cursor(self):
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return connection, cursor

    def close(self):
        self.connection.close()
        return self.cursor.lastrowid