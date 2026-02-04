from src.services.subject_service import SubjectService


def display_menu():
    print("\n" + "="*40)
    print("       MENU SUBJECT")
    print("="*40)
    print("1. Creer une matiere")
    print("2. Afficher une matiere par ID")
    print("3. Afficher toutes les matieres")
    print("4. Modifier une matiere")
    print("5. Supprimer une matiere")
    print("6. Quitter")
    print("="*40)


def create_view(service: SubjectService):
    print("\n--- CREER UNE MATIERE ---")
    name = input("Nom: ")
    coefficient = input("Coefficient: ")
    
    try:
        coefficient = float(coefficient)
        subject = service.create(name, coefficient)
        
        if subject:
            print(f"Matiere creee avec succes: {subject}")
        else:
            print("Erreur lors de la creation!")
    except ValueError:
        print("Coefficient invalide! Entrer un nombre.")


def get_by_id_view(service: SubjectService):
    print("\n--- AFFICHER MATIERE PAR ID ---")
    subject_id = input("ID de la matiere: ")
    
    try:
        subject_id = int(subject_id)
        subject = service.get_by_id(subject_id)
        
        if subject:
            print(f"\nID: {subject.id}")
            print(f"Nom: {subject.name}")
            print(f"Coefficient: {subject.coefficient}")
            print(f"Created at: {subject.created_at}")
        else:
            print("Matiere introuvable!")
    except ValueError:
        print("ID invalide!")


def get_all_view(service: SubjectService):
    print("\n--- LISTE DES MATIERES ---")
    subjects = service.get_all()
    
    if subjects:
        for subject in subjects:
            print(f"- {subject}")
    else:
        print("Aucune matiere trouvee")


def update_view(service: SubjectService):
    print("\n--- MODIFIER UNE MATIERE ---")
    subject_id = input("ID de la matiere: ")
    
    try:
        subject_id = int(subject_id)
        subject = service.get_by_id(subject_id)
        
        if not subject:
            print("Matiere introuvable!")
            return
        
        print(f"Matiere actuelle: {subject}")
        name = input("Nouveau nom (vide pour garder): ")
        coefficient_str = input("Nouveau coefficient (vide pour garder): ")
        
        coefficient = None
        if coefficient_str:
            try:
                coefficient = float(coefficient_str)
            except ValueError:
                print("Coefficient invalide!")
                return
        
        success = service.update(
            subject_id,
            name if name else None,
            coefficient
        )
        
        if success:
            print("Matiere modifiee avec succes!")
        else:
            print("Erreur lors de la modification!")
    except ValueError:
        print("ID invalide!")


def delete_view(service: SubjectService):
    print("\n--- SUPPRIMER UNE MATIERE ---")
    subject_id = input("ID de la matiere: ")
    
    try:
        subject_id = int(subject_id)
        confirm = input(f"Confirmer la suppression de la matiere {subject_id}? (o/n): ")
        
        if confirm.lower() == 'o':
            success = service.delete(subject_id)
            if success:
                print("Matiere supprimee avec succes!")
            else:
                print("Matiere introuvable!")
        else:
            print("Suppression annulee")
    except ValueError:
        print("ID invalide!")


def main():
    service = SubjectService()
    
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
