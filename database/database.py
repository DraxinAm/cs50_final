import sqlite3

class Database:
    def __init__(self, db_file="database/recipes.db"):
        self.db_file = db_file

    def search(self, recipe_title):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT id FROM recipes WHERE title = ?", (recipe_title,))
        recipe_id = cursor.fetchone()[0]
        cursor.execute("SELECT ")
        

    def insert_recipes(self, user_id, recipe_title, description, cooktime, servings):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("INSERT INTO recipes (user_id, title, description, servings, cook_time) VALUES (?, ?, ?, ?, ?)", (user_id, recipe_title, description, cooktime, servings))
        connection.commit()
        connection.close()

    def insert_tags(self, recipe_title, tags):
        connection, cursor = self.connection_and_cursor()
        for tag in tags:
            cursor.execute("INSERT INTO recipe_tags (recipe_id, tag_id) VALUES ((SELECT id FROM recipes WHERE title = ?), (SELECT id FROM tags WHERE name = ?))", (recipe_title, tag))
        connection.commit()
        connection.close()

    def insert_ingredients(self, recipe_title, ingredients):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT id FROM recipes WHERE title = ?", (recipe_title,))
        recipe_id = cursor.fetchone()[0]
        for i in range(len(ingredients)):
            ing = ingredients[i]
            cursor.execute("INSERT INTO ingredients(recipe_id, amount, unit, name) VALUES (?, ?, ?, ?)", (recipe_id, ing["amount"], ing["unit"], ing["name"]))
        connection.commit()
        connection.close()

    def insert_steps(self, recipe_title, steps):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT id FROM recipes WHERE title = ?", (recipe_title,))
        recipe_id = cursor.fetchone()[0]
        for i in range(len(steps)):
            cursor.execute("INSERT INTO steps (recipe_id, step_number, instruction) VALUES (?, ?, ?)", (recipe_id, i + 1, steps[i]))
        connection.commit()
        connection.close()

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