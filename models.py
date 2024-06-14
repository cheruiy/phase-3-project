import sqlite3

# Class to manage users in the database
class Users:
    def __init__(self, db_file):
        self._db_file = db_file

    @property
    def db_file(self):
        return self._db_file

    @db_file.setter
    def db_file(self, value):
        self._db_file = value

    def save(self, query, params):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def add_user(self, name):
        query = 'INSERT INTO users (name) VALUES (?)'
        self.save(query, (name,))
        print(f"User {name} added.")

    def list_users(self):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM users')
            users = cursor.fetchall()
            if not users:
                print("No users available.")
                return
            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]}")

    def delete_user(self, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            print("Invalid user ID. Please provide a valid integer ID.")
            return

        query = 'DELETE FROM users WHERE id = ?'
        self.save(query, (user_id,))
        query = 'DELETE FROM user_shopping_lists WHERE user_id = ?'
        self.save(query, (user_id,))
        print(f"User with ID {user_id} deleted.")

# Class to manage shopping lists in the database
class ShoppingLists:
    def __init__(self, db_file):
        self._db_file = db_file

    @property
    def db_file(self):
        return self._db_file

    @db_file.setter
    def db_file(self, value):
        self._db_file = value

    def save(self, query, params):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def add_shopping_list(self, user_id, name):
        query = 'INSERT INTO shopping_lists (user_id, name) VALUES (?, ?)'
        self.save(query, (user_id, name))
        print(f"Shopping list {name} added for user ID {user_id}.")

    def add_user_to_shopping_list(self, user_id, shopping_list_id):
        query = 'INSERT INTO user_shopping_lists (user_id, shopping_list_id) VALUES (?, ?)'
        self.save(query, (user_id, shopping_list_id))
        print(f"User ID {user_id} added to shopping list ID {shopping_list_id}.")

    def list_shopping_lists(self):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM shopping_lists')
            shopping_lists = cursor.fetchall()
            if not shopping_lists:
                print("No shopping lists found.")
                return
            for shopping_list in shopping_lists:
                print(f"ID: {shopping_list[0]}, Name: {shopping_list[1]}")

    def delete_shopping_list(self, list_id):
        try:
            list_id = int(list_id)
        except ValueError:
            print("Invalid shopping list ID. Please provide a valid integer ID.")
            return

        query = 'DELETE FROM shopping_lists WHERE id = ?'
        self.save(query, (list_id,))
        query = 'DELETE FROM user_shopping_lists WHERE shopping_list_id = ?'
        self.save(query, (list_id,))
        query = 'DELETE FROM shopping_list_items WHERE shopping_list_id = ?'
        self.save(query, (list_id,))
        print(f"Shopping list with ID {list_id} deleted.")

# Class to manage items in the database
class Items:
    def __init__(self, db_file):
        self._db_file = db_file

    @property
    def db_file(self):
        return self._db_file

    @db_file.setter
    def db_file(self, value):
        self._db_file = value

    def save(self, query, params):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def add_item(self, name, quantity):
        query = 'INSERT INTO items (name, quantity) VALUES (?, ?)'
        self.save(query, (name, quantity))
        print(f"Item {name} with quantity {quantity} added.")

    def list_items(self):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, quantity FROM items')
            items = cursor.fetchall()
            if not items:
                print(f"No items found.")
                return
            for item in items:
                print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")

    def remove_item(self, item_id):
        query = 'DELETE FROM items WHERE id = ?'
        self.save(query, (item_id,))
        print(f"Item with ID {item_id} removed.")

# Class to manage the entire shopping list system
class ShoppingListManager:
    def __init__(self, db_file='cli.db'):
        self._db_file = db_file
        self.users = Users(db_file)
        self.shopping_lists = ShoppingLists(db_file)
        self.items = Items(db_file)
        self.create_tables()

    @property
    def db_file(self):
        return self._db_file

    @db_file.setter
    def db_file(self, value):
        self._db_file = value
        self.users.db_file = value
        self.shopping_lists.db_file = value
        self.items.db_file = value

    def create_tables(self):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS shopping_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_shopping_lists (
                user_id INTEGER NOT NULL,
                shopping_list_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists (id),
                PRIMARY KEY (user_id, shopping_list_id)
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS shopping_list_items (
                shopping_list_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists (id),
                FOREIGN KEY (item_id) REFERENCES items (id),
                PRIMARY KEY (shopping_list_id, item_id)
            )''')
            conn.commit()

    def add_item_to_shopping_list(self, shopping_list_id, item_id, quantity):
        self.items.save('INSERT INTO shopping_list_items (shopping_list_id, item_id, quantity) VALUES (?, ?, ?)', (shopping_list_id, item_id, quantity))
        print(f"Item ID {item_id} with quantity {quantity} added to shopping list ID {shopping_list_id}.")

    def list_tables(self):
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if not tables:
                print("No tables found.")
                return
            print("Tables in the database:")
            for table in tables:
                print(table[0])

    def display_help(self):
        help_text = """
        Available commands:
        1. Add User: add-user [name]
        2. Add Shopping List: add-shopping-list [user_id] [name]
        3. Add Item: add-item [name] [quantity]
        4. List Users: list-users
        5. List Shopping Lists: list-shopping-lists
        6. List Items: list-items
        7. Remove Item: remove-item [item_id]
        8. Add User to Shopping List: add-user-to-shopping-list [user_id] [shopping_list_id]
        9. Add Item to Shopping List: add-item-to-shopping-list [shopping_list_id] [item_id] [quantity]
         10. List Tables: list-tables
         11. Delete User: delete-user [user_id]
         12. Delete Shopping List: delete-shopping-list [shopping_list_id]
         13. Exit: exit
         """
        print(help_text)
