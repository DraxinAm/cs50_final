import sqlite3

class Database:
    def __init__(self, db_file="recipes.db"):
        self.db_file = db_file

    def execute(self, query, params=()):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        # return a list of dicts
        self.connection.row_maker = sqlite3.Row
        self.cursor.execute(query, params)
        
        if query.strip().upper().startswith("SELECT"):
            result = self.cursor.fetchall()
            self.connection.close()
            return [dict(row) for row in result]

    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()
        return self.cursor.lastrowid
