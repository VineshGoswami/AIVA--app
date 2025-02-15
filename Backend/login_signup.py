from authenticator import signin, register


def main():
    print("Welcome to AIVA Assistant Login System")

    while True:
        print("\n1. Signup\n2. Login (Password + Face Recognition)\n3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            image_path = input("Enter image path for face recognition: ").strip()
            message = signup(username, password, image_path)
            print(message)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            login_status = login(username, password)
            if login_status == f"Login successful. Welcome, {username}!":
                print(login_status)
                break
            else:
                print(login_status)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()
