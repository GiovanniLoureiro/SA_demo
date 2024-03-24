import sqlite3

conn = sqlite3.connect("/Users/gio/Desktop/SA_demo/backend/main.db")
cur = conn.cursor()

# Create tables if they don't exist
cur.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, user TEXT, description TEXT, type TEXT);")
cur.execute("CREATE TABLE IF NOT EXISTS permissions (id INTEGER PRIMARY KEY, user TEXT, permission TEXT, type TEXT);")

# Insert data
cur.execute("INSERT INTO files (id, user, description, type) VALUES (1, 'user1', 'Change button color to blue', 'file'), (2, 'user2', 'Fix payment delay bug', 'file'), (3, 'user1', 'Add Flask to req', 'prescription'), (4, 'user3', 'Add permissions to req', 'file');")
cur.execute("INSERT INTO permissions (id, user, permission, type) VALUES (1, 'user1', 'user1', 'all'), (2, 'user2', 'user2', 'all'), (3, 'gp1', 'user1', 'all'), (4, 'gp1', 'user2', 'all'), (5, 'user3', 'user3', 'all'), (6, 'pharma1', 'user1', 'prescription');")

# Commit the transaction to save changes
conn.commit()

# Query to check data
data = cur.execute("SELECT * FROM files")
for row in data:
    print(row)

# Close cursor and connection
cur.close()
conn.close()
