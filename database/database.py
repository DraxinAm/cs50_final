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

    def execute(self, query, params=()):
        # connect to the database
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        # return a list of dicts
        self.connection.row_factory = sqlite3.Row
        try:
            # Execute the sql queries with preparation to avoid sql injection
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.close()
        
        if query.strip().upper().startswith("SELECT"):
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            # Fetch all results
            result = self.cursor.fetchall()
            print(result)
            # Close the connection
            self.connection.close()
            # Convert sqlite3.Row objects to dictionaries
            return [dict(row) for row in result]
        
    def get_user_by_username(self, username):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        result = dict(result)
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