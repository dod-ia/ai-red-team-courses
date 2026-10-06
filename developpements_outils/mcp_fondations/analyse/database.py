from pathlib import Path
import sqlite3
import string
import random

def init_database() -> str:
    """
    Create a SQLite database and fill it with fake data.
    2 tables: users (name,password), orders(name,product)
    The database is stored in a file `enterprise_database.db` in the current repertory.
    """

    if Path("./enterprise_database.db").exists():
        print("Database already created - Ignore creation")
        return "enterprise_database.db"

    print("Create the database...")
    connection = sqlite3.connect("./enterprise_database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, password TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, product TEXT NOT NULL)""")

    list_users = ["Lion El'Jonson", "Fulgrim", "Perturabo", "Jaghatai Khan", "Leman Russ", "Rogal Dorn", "Konrad Curze", 
                  "Sanguinius", "Ferrus Manus", "Angron", "Roboute Guilliman", "Mortarion", "Magnus le Rouge", "Horus Lupercal", 
                  "Lorgar Aurelian", "Vulkan", "Corvus Corax", "Alpharius Omegon"]

    list_products = ["Rhino", "Razorback", "Predator", "Vindicator", "Land Raider", "Repulsor", 
                     "Impulsor", "Gladiator", "Dreadnought", "Redemptor Dreadnought"]

    for name in list_users:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))

    for orders in range(50):
        name = random.choice(list_users)
        product = random.choice(list_products)
        cursor.execute("INSERT INTO orders (name, product) VALUES (?, ?)", (name, product))     

    connection.commit()
    print("Database created.")

    cursor.execute("SELECT COUNT(*) FROM users")
    nb_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    nb_orders = cursor.fetchone()[0]

    print(f"Database - users: {nb_users}, orders: {nb_orders}")

    cursor.close()
    connection.commit()
    connection.close()
    return "enterprise_database.db"