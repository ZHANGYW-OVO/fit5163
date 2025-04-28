from auth import register, login
from ehr_record import initialize_system

def main():
    initialize_system()

    while True:
        print("\n=== Welcome to Secure EHR System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()