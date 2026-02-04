from src.services.user_service import UserService


def display_menu():
    print("\n" + "="*40)
    print("       MENU PRINCIPAL")
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. Me (Current User)")
    print("5. Quitter")
    print("="*40)


def register_view(service: UserService):
    print("\n--- REGISTER ---")
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (admin/staff) [staff]: ") or "staff"
    
    user = service.register(username, password, role)
    
    if user:
        print(f"User cree avec succes: {user}")
    else:
        print("Erreur: Username deja existant!")


def login_view(service: UserService):
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")
    
    success = service.login(username, password)
    
    if success:
        print(f"Connecte avec succes!")
        print(f"Welcome {service.current_user.username} ({service.current_user.role})")
    else:
        print("Username ou password incorrect!")


def logout_view(service: UserService):
    if not service.is_logged_in:
        print("Vous n'etes pas connecte!")
        return
    
    print(f"\n--- LOGOUT ---")
    print(f"Au revoir {service.current_user.username}!")
    service.logout()
    print("Deconnecte avec succes!")


def me_view(service: UserService):
    print("\n--- CURRENT USER ---")
    user = service.me()
    
    if user:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")
        print(f"Created at: {user.created_at}")
        print(f"Status: Connecte")
    else:
        print("Aucun utilisateur connecte")


def main():
    service = UserService()
    
    while True:
        display_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            register_view(service)
        elif choice == "2":
            login_view(service)
        elif choice == "3":
            logout_view(service)
        elif choice == "4":
            me_view(service)
        elif choice == "5":
            print("\nAu revoir!")
            break
        else:
            print("Option invalide!")


if __name__ == "__main__":
    main()
