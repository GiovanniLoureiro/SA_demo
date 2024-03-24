from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = '/Users/gio/Desktop/SA_demo/backend/main.db'

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Function to get permissions
def get_permissions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM permissions")
    permissions = cur.fetchall()  # Fetch all results at once
    permissions_list = [dict(row) for row in permissions]  # Convert to list of dicts
    cur.close()
    conn.close()
    return permissions_list

# Function to get files
def get_files():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")
    files = cur.fetchall()  # Fetch all results at once
    files_list = [dict(row) for row in files]  # Convert to list of dicts
    cur.close()
    conn.close()
    return files_list

# Example usage
permissions_list = get_permissions()
files_list = get_files()

print("Permissions:")
for perm in permissions_list:
    print(perm)

print("Files:")
for file in files_list:
    print(file)

# Login route remains the same

# Counter for generating unique IDs for new files
cid = 4

# A simple users database. In production, use a secure password handling and storage mechanism.
users = [
    {"username": "gp1", "password": "pass"},
    {"username": "user1", "password": "pass"},
    {"username": "user2", "password": "pass"},
    {"username": "user3", "password": "pass"},
    {"username": "pharma1", "password": "pass"},
]


# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({"message": "Could not verify", "WWW-Authenticate": "Basic realm='Login required'"}), 401

    user = next(
        (user for user in users if user['username'] == auth['username'] and user['password'] == auth['password']), None)
    if not user:
        # If the user is not found or password does not match
        return jsonify({"message": "Invalid username or password"}), 403

    return jsonify({"message": "Login successful"})

@app.route("/get_files")
def get_files():
    username = request.args.get('username')

    # Find the permissions for the requesting user
    user_permissions = [perm for perm in permissions_list if perm["user"] == username]

    # Collect users and their accessible file types based on permissions
    accessible_files = {}
    for perm in user_permissions:
        if perm["type"] == "all":
            accessible_files[perm["permission"]] = "all"
        elif perm["type"] == "prescription":
            if perm["permission"] not in accessible_files or accessible_files[perm["permission"]] != "all":
                accessible_files[perm["permission"]] = "prescription"
    print(f"files {accessible_files}")

    # Filter files based on the accessible types determined above
    filtered_files = [
        file for file in files_list
        if file["user"] in accessible_files and (
            accessible_files[file["user"]] == "all" or file["type"] == accessible_files[file["user"]])
    ]
    print(f"filtered files {filtered_files}")
    return jsonify({"files": filtered_files})



# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
