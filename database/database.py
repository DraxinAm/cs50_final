import sqlite3

class Database:
    def __init__(self, db_file="recipes.db"):
        self.db_file = db_file

    def execute(self, query, params=()):
        # connect to the database
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        # return a list of dicts
        self.connection.row_maker = sqlite3.Row
        try:
            # Execute the sql queries with preparation to avoid sql injection
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.close()
        
        if query.strip().upper().startswith("SELECT"):
             # Fetch all results
            result = self.cursor.fetchall()
            # Close the connection
            self.connection.close()
            # Convert sqlite3.Row objects to dictionaries
            return [dict(row) for row in result]

    def close(self):
        self.connection.close()
        return self.cursor.lastrowid
