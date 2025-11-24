import sqlite3

class Database:
    def __init__(self, db_file="database/recipes.db"):
        self.db_file = db_file

    def list_recipe(self, user_id):
        connection, cursor = self.connection_and_cursor()
        # Title and description
        cursor.execute("SELECT id, title, description FROM recipes WHERE user_id = ? ORDER BY created_at DESC ", (user_id,))
        result = cursor.fetchall()
        cards = []
        for i in result:
            cards.append(dict(i))
        connection.commit()
        connection.close()
        return cards
        
    def return_recipe_info(self, recipe_id):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT title, description, servings, cook_time FROM recipes WHERE id = ?", (recipe_id, ))
        result = cursor.fetchone()
        info = dict(result)
        cursor.execute("SELECT name FROM tags WHERE ID IN (SELECT tag_id FROM recipe_tags WHERE recipe_id = ?)", (recipe_id, ))
        result = cursor.fetchall()
        tags = []
        for i in result:
            tags.append(dict(i)) if result else {}
        cursor.execute("SELECT amount, unit, name FROM ingredients WHERE recipe_id = ?", (recipe_id, ))
        result = cursor.fetchall()
        ingredients = []
        for i in result:
            ingredients.append(dict(i)) if result else {}
        cursor.execute("SELECT instruction FROM steps WHERE recipe_id = ? ORDER BY step_number ASC", (recipe_id, ))
        result = cursor.fetchall()
        steps = []
        for i in result:
            steps.append(dict(i)) if result else {}
        connection.commit()
        connection.close()
        return info, tags, ingredients, steps 
    


    def search(self, recipe_title):
        connection, cursor = self.connection_and_cursor()
        cursor.execute("SELECT id, title, description FROM recipes WHERE title LIKE ?", (f"%{recipe_title}%",))
        result = cursor.fetchall()
        cards = []
        for i in result:
            cards.append(dict(i))
        connection.commit()
        connection.close()
        return cards
        # Search for 
        #cursor.execute("SELECT ")
        

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