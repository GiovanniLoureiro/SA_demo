import csv

from flask import Flask, jsonify, request

app = Flask(__name__)


# Function to read get_files from a CSV file
def read_files_from_csv():
    files_list = []
    with open('files.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            files_list.append(row)
    return files_list


# Function to read permissions from a CSV file
def read_permissions_from_csv():
    permissions_list = []
    with open('permissions.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            permissions_list.append(row)
    return permissions_list


# Global variable to store permissions, initially loaded from CSV
permissions_list = read_permissions_from_csv()
print("perms:")
print(permissions_list)

# Global variable to store get_files, initially loaded from CSV
files_list = read_files_from_csv()

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

    # Read permissions from CSV (or use global variable if already loaded)
    permissions_list = read_permissions_from_csv()

    # Find the permissions for the requesting user
    user_permissions = [perm for perm in permissions_list if perm["user"] == username]

    # Collect users and their accessible file types based on permissions
    accessible_files = {}
    for perm in user_permissions:
        if perm["type"] == "all":
            accessible_files[perm["permission"]] = "all"
        elif perm["type"] == "prescription":
            # Assuming a user could have 'all' and 'prescription' permissions separately
            if perm["permission"] not in accessible_files or accessible_files[perm["permission"]] != "all":
                accessible_files[perm["permission"]] = "prescription"

    # Filter files based on the accessible types determined above
    filtered_files = [
        file for file in files_list
        if file["user"] in accessible_files and (
                    accessible_files[file["user"]] == "all" or file["type"] == accessible_files[file["user"]])
    ]

    return jsonify({"files": filtered_files})

    return jsonify({"files": filtered_files})


# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
