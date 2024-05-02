import sqlite3

# Path to your SQLite database
db_path = 'C:/Users/Jarvis/Desktop/DJANGO/Real-Estate-Django-Web-App/db.sqlite3'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# List all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection to the database
conn.close()
