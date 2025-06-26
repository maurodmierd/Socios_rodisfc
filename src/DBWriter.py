import sqlite3

database_path = "example.db"

try:
    conn = sqlite3.connect(database_path)
    print(f"Successfully connected to {database_path}")

    # Example usage: Execute a query
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM socios")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    conn.close()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")