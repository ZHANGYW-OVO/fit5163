import json
import os
from audit_log import write_log
from ehr_record import patient_menu, doctor_menu, admin_menu

USERS_FILE = "users.json"
current_user = None

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def register():
    users = load_users()
    username = input("Enter new username: ")
    if username in users:
        print("❌ Username already exists.")
        return
    password = input("Enter password: ")
    print("Select role: ")
    print("1. Patient")
    print("2. Doctor")
    print("3. Admin")
    role_map = {"1": "patient", "2": "doctor", "3": "admin"}
    role = role_map.get(input("Enter choice (1-3): "))

    if not role:
        print("❌ Invalid role choice.")
        return

    user_info = {"password": password, "role": role}
    if role == "doctor":
        user_info["patients"] = input("Enter usernames of patients this doctor will manage (comma separated): ").split(",")
        user_info["patients"] = [p.strip() for p in user_info["patients"]]

    users[username] = user_info
    save_users(users)
    print(f"✅ User '{username}' registered successfully as {role.capitalize()}!")

def login():
    global current_user
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username]["password"] == password:
        current_user = {"username": username, "role": users[username]["role"]}
        if "patients" in users[username]:
            current_user["patients"] = users[username]["patients"]
        print(f"✅ Login successful! Welcome, {username} ({current_user['role'].capitalize()})")
        role_menu()
    else:
        print("❌ Invalid username or password.")

def logout():
    global current_user
    current_user = None
    print("✅ Logged out successfully.")

def role_menu():
    if current_user["role"] == "patient":
        patient_menu(current_user)
    elif current_user["role"] == "doctor":
        doctor_menu(current_user)
    elif current_user["role"] == "admin":
        admin_menu(current_user)
    else:
        print("❌ Unknown role!")