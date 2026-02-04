from src.services.class_service import ClassService


def display_menu():
    print("\n" + "="*40)
    print("       MENU CLASS")
    print("="*40)
    print("1. Creer une classe")
    print("2. Afficher une classe par ID")
    print("3. Afficher toutes les classes")
    print("4. Modifier une classe")
    print("5. Supprimer une classe")
    print("6. Quitter")
    print("="*40)


def create_view(service: ClassService):
    print("\n--- CREER UNE CLASSE ---")
    name = input("Nom: ")
    level = input("Niveau: ")
    year = input("Annee: ")
    
    class_obj = service.create(name, level, year)
    
    if class_obj:
        print(f"Classe creee avec succes: {class_obj}")
    else:
        print("Erreur lors de la creation!")


def get_by_id_view(service: ClassService):
    print("\n--- AFFICHER CLASSE PAR ID ---")
    class_id = input("ID de la classe: ")
    
    try:
        class_id = int(class_id)
        class_obj = service.get_by_id(class_id)
        
        if class_obj:
            print(f"\nID: {class_obj.id}")
            print(f"Nom: {class_obj.name}")
            print(f"Niveau: {class_obj.level}")
            print(f"Annee: {class_obj.year}")
            print(f"Created at: {class_obj.created_at}")
        else:
            print("Classe introuvable!")
    except ValueError:
        print("ID invalide!")


def get_all_view(service: ClassService):
    print("\n--- LISTE DES CLASSES ---")
    classes = service.get_all()
    
    if classes:
        for class_obj in classes:
            print(f"- {class_obj}")
    else:
        print("Aucune classe trouvee")


def update_view(service: ClassService):
    print("\n--- MODIFIER UNE CLASSE ---")
    class_id = input("ID de la classe: ")
    
    try:
        class_id = int(class_id)
        class_obj = service.get_by_id(class_id)
        
        if not class_obj:
            print("Classe introuvable!")
            return
        
        print(f"Classe actuelle: {class_obj}")
        name = input("Nouveau nom (vide pour garder): ")
        level = input("Nouveau niveau (vide pour garder): ")
        year = input("Nouvelle annee (vide pour garder): ")
        
        success = service.update(
            class_id,
            name if name else None,
            level if level else None,
            year if year else None
        )
        
        if success:
            print("Classe modifiee avec succes!")
        else:
            print("Erreur lors de la modification!")
    except ValueError:
        print("ID invalide!")


def delete_view(service: ClassService):
    print("\n--- SUPPRIMER UNE CLASSE ---")
    class_id = input("ID de la classe: ")
    
    try:
        class_id = int(class_id)
        confirm = input(f"Confirmer la suppression de la classe {class_id}? (o/n): ")
        
        if confirm.lower() == 'o':
            success = service.delete(class_id)
            if success:
                print("Classe supprimee avec succes!")
            else:
                print("Classe introuvable!")
        else:
            print("Suppression annulee")
    except ValueError:
        print("ID invalide!")


def main():
    service = ClassService()
    
    while True:
        display_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            create_view(service)
        elif choice == "2":
            get_by_id_view(service)
        elif choice == "3":
            get_all_view(service)
        elif choice == "4":
            update_view(service)
        elif choice == "5":
            delete_view(service)
        elif choice == "6":
            print("\nAu revoir!")
            break
        else:
            print("Option invalide!")


if __name__ == "__main__":
    main()
