import json
import os
from encryption import initialize_key, load_key, encrypt_data, decrypt_data
from audit_log import write_log

RECORDS_FILE = "records.json"

def load_records():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_records(records):
    with open(RECORDS_FILE, "w") as f:
        json.dump(records, f, indent=4)

def initialize_system():
    initialize_key()
    if not os.path.exists(RECORDS_FILE):
        save_records({})

def patient_menu(current_user):
    key = load_key()
    records = load_records()
    username = current_user["username"]
    while True:
        print("\n--- Patient Menu ---")
        print("1. View My Health Record")
        print("2. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            if username in records:
                print("\n--- Your Health Records ---")
                for idx, record in enumerate(records[username]):
                    decrypted = decrypt_data(key, record)
                    print(f"Record {idx + 1}: {decrypted}")
                write_log(f"Patient {username} viewed their health records.")
            else:
                print("No records found for your account.")
                write_log(f"Patient {username} attempted to view records but none were found.")
        elif choice == "2":
            from auth import logout
            logout()
            break
        else:
            print("❌ Invalid choice.")

def doctor_menu(current_user):
    key = load_key()
    records = load_records()

    while True:
        print("\n--- Doctor Menu ---")
        print("1. View Managed Patients")
        print("2. Add Patient Record")
        print("3. Update Patient Record")
        print("4. Delete Patient Record")
        print("5. Add/Remove Managed Patient")
        print("6. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            # 查看管理的病人
            print("Managed Patients:")
            for patient in current_user.get("patients", []):
                if patient in records:
                    for idx, record in enumerate(records[patient]):
                        decrypted = decrypt_data(key, record)
                        print(f"- {patient} Record {idx+1}: {decrypted}")
                    write_log(f"Doctor {current_user['username']} viewed records of patient {patient}.")
                else:
                    print(f"- {patient}: No record found.")
                    write_log(f"Doctor {current_user['username']} attempted to view records of patient {patient} but none were found.")

        elif choice == "2":
            # 添加病人记录
            patient = input("Enter patient username: ")
            if patient in current_user.get("patients", []):
                diagnosis = input("Enter diagnosis: ")
                prescription = input("Enter prescription: ")
                new_data = {"diagnosis": diagnosis, "prescription": prescription}
                encrypted_data = encrypt_data(key, new_data)
                if patient not in records:
                    records[patient] = []
                records[patient].append(encrypted_data)
                save_records(records)
                print(f"Record added for {patient}")
                write_log(f"Doctor {current_user['username']} added a record for patient {patient}")
            else:
                print(f"Error: You do not manage patient {patient}.")
                write_log(f"Doctor {current_user['username']} attempted to add a record for non-managed patient {patient}")

        elif choice == "3":
            # 更新病人记录
            patient = input("Enter patient username: ")
            if patient in current_user.get("patients", []):
                if patient in records:
                    for idx, record in enumerate(records[patient]):
                        decrypted = decrypt_data(key, record)
                        print(f"{idx+1}: {decrypted}")
                    record_idx = int(input("Enter record number to update: ")) - 1
                    if 0 <= record_idx < len(records[patient]):
                        diagnosis = input("Enter new diagnosis: ")
                        prescription = input("Enter new prescription: ")
                        updated_data = {"diagnosis": diagnosis, "prescription": prescription}
                        records[patient][record_idx] = encrypt_data(key, updated_data)
                        save_records(records)
                        print(f"Record {record_idx+1} updated for {patient}")
                        write_log(f"Doctor {current_user['username']} updated record {record_idx+1} of patient {patient}")
                    else:
                        print("Invalid record number.")
                else:
                    print("No records found for this patient.")
            else:
                print(f"Error: You do not manage patient {patient}.")
                write_log(f"Doctor {current_user['username']} attempted to update a record for non-managed patient {patient}")

        elif choice == "4":
            # 删除病人记录
            patient = input("Enter patient username: ")
            if patient in current_user.get("patients", []):
                if patient in records:
                    for idx, record in enumerate(records[patient]):
                        decrypted = decrypt_data(key, record)
                        print(f"{idx+1}: {decrypted}")
                    record_idx = int(input("Enter record number to delete: ")) - 1
                    if 0 <= record_idx < len(records[patient]):
                        del records[patient][record_idx]
                        save_records(records)
                        print(f"Record {record_idx+1} deleted for {patient}")
                        write_log(f"Doctor {current_user['username']} deleted record {record_idx+1} of patient {patient}")
                    else:
                        print("Invalid record number.")
                else:
                    print("No records found for this patient.")
            else:
                print(f"Error: You do not manage patient {patient}.")
                write_log(f"Doctor {current_user['username']} attempted to delete a record for non-managed patient {patient}")

        elif choice == "5":
            # 添加/移除管理的病人
            action = input("Enter 'add' to add a patient or 'remove' to remove a patient: ").strip().lower()
            patient = input("Enter patient username: ").strip()
            if action == "add":
                if patient not in current_user.get("patients", []):
                    current_user["patients"].append(patient)
                    print(f"Patient {patient} added to your managed list.")
                    write_log(f"Doctor {current_user['username']} added patient {patient} to managed list.")
                else:
                    print("Patient already in your managed list.")
            elif action == "remove":
                if patient in current_user.get("patients", []):
                    current_user["patients"].remove(patient)
                    print(f"Patient {patient} removed from your managed list.")
                    write_log(f"Doctor {current_user['username']} removed patient {patient} from managed list.")
                else:
                    print("Patient not in your managed list.")
            else:
                print("Invalid action.")

        elif choice == "6":
            # 登出
            from auth import logout
            logout()
            break

        else:
            print("Invalid choice.")



def admin_menu(current_user):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add New User")
        print("2. View Audit Logs")
        print("3. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            from auth import register
            register()
        elif choice == "2":
            if os.path.exists("audit.log"):
                with open("audit.log", "r") as f:
                    print(f.read())
            else:
                print("No audit logs found.")
        elif choice == "3":
            from auth import logout
            logout()
            break
        else:
            print("❌ Invalid choice.")