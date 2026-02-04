from datetime import date
from src.services.student_service import StudentService
from src.services.class_service import ClassService


def display_menu():
    print("\n" + "="*40)
    print("       MENU STUDENT")
    print("="*40)
    print("1. Creer un etudiant")
    print("2. Afficher un etudiant par ID")
    print("3. Afficher tous les etudiants")
    print("4. Afficher tous les etudiants avec classe")
    print("5. Modifier un etudiant")
    print("6. Supprimer un etudiant")
    print("7. Quitter")
    print("="*40)


def select_class(class_service: ClassService) -> int:
    print("\n--- SELECTIONNER UNE CLASSE ---")
    classes = class_service.get_all()
    
    if not classes:
        print("Aucune classe disponible! Veuillez creer une classe d'abord.")
        return 0
    
    print("\nClasses disponibles:")
    for class_obj in classes:
        print(f"{class_obj.id}. {class_obj.name} - {class_obj.level} - {class_obj.year}")
    
    while True:
        try:
            class_id = int(input("\nChoisir l'ID de la classe: "))
            if any(c.id == class_id for c in classes):
                return class_id
            else:
                print("ID invalide! Choisir parmi les classes affichees.")
        except ValueError:
            print("Entrer un numero valide!")


def create_view(student_service: StudentService, class_service: ClassService):
    print("\n--- CREER UN ETUDIANT ---")
    
    class_id = select_class(class_service)
    if class_id == 0:
        return
    
    first_name = input("Prenom: ")
    last_name = input("Nom: ")
    email = input("Email: ")
    phone = input("Telephone: ")
    date_birth = input("Date de naissance (YYYY-MM-DD): ")
    
    try:
        date_of_birth = date.fromisoformat(date_birth)
        student = student_service.create(first_name, last_name, email, phone, date_of_birth, class_id)
        
        if student:
            print(f"Etudiant cree avec succes: {student}")
        else:
            print("Erreur lors de la creation! Email peut-etre deja existant.")
    except ValueError:
        print("Date invalide! Format: YYYY-MM-DD")


def get_by_id_view(student_service: StudentService):
    print("\n--- AFFICHER ETUDIANT PAR ID ---")
    student_id = input("ID de l'etudiant: ")
    
    try:
        student_id = int(student_id)
        student = student_service.get_by_id(student_id)
        
        if student:
            print(f"\nID: {student.id}")
            print(f"Nom complet: {student.first_name} {student.last_name}")
            print(f"Email: {student.email}")
            print(f"Telephone: {student.phone}")
            print(f"Date de naissance: {student.date_of_birth}")
            print(f"Class ID: {student.class_id}")
            print(f"Created at: {student.created_at}")
        else:
            print("Etudiant introuvable!")
    except ValueError:
        print("ID invalide!")


def get_all_view(student_service: StudentService):
    print("\n--- LISTE DES ETUDIANTS ---")
    students = student_service.get_all()
    
    if students:
        for student in students:
            print(f"- {student}")
    else:
        print("Aucun etudiant trouve")


def get_all_with_class_view(student_service: StudentService):
    print("\n--- LISTE DES ETUDIANTS AVEC CLASSE ---")
    results = student_service.get_all_with_class()
    
    if results:
        for result in results:
            student = result['student']
            print(f"\n- ID: {student.id} | {student.first_name} {student.last_name}")
            print(f"  Email: {student.email} | Phone: {student.phone}")
            if result['class_name']:
                print(f"  Classe: {result['class_name']} - {result['class_level']} - {result['class_year']}")
            else:
                print(f"  Classe: Non trouvee")
    else:
        print("Aucun etudiant trouve")


def update_view(student_service: StudentService, class_service: ClassService):
    print("\n--- MODIFIER UN ETUDIANT ---")
    student_id = input("ID de l'etudiant: ")
    
    try:
        student_id = int(student_id)
        student = student_service.get_by_id(student_id)
        
        if not student:
            print("Etudiant introuvable!")
            return
        
        print(f"Etudiant actuel: {student}")
        first_name = input("Nouveau prenom (vide pour garder): ")
        last_name = input("Nouveau nom (vide pour garder): ")
        email = input("Nouveau email (vide pour garder): ")
        phone = input("Nouveau telephone (vide pour garder): ")
        date_birth = input("Nouvelle date de naissance YYYY-MM-DD (vide pour garder): ")
        
        change_class = input("Changer de classe? (o/n): ")
        class_id = None
        if change_class.lower() == 'o':
            class_id = select_class(class_service)
            if class_id == 0:
                class_id = None
        
        date_of_birth = None
        if date_birth:
            try:
                date_of_birth = date.fromisoformat(date_birth)
            except ValueError:
                print("Date invalide! Format: YYYY-MM-DD")
                return
        
        success = student_service.update(
            student_id,
            first_name if first_name else None,
            last_name if last_name else None,
            email if email else None,
            phone if phone else None,
            date_of_birth,
            class_id
        )
        
        if success:
            print("Etudiant modifie avec succes!")
        else:
            print("Erreur lors de la modification!")
    except ValueError:
        print("ID invalide!")


def delete_view(student_service: StudentService):
    print("\n--- SUPPRIMER UN ETUDIANT ---")
    student_id = input("ID de l'etudiant: ")
    
    try:
        student_id = int(student_id)
        confirm = input(f"Confirmer la suppression de l'etudiant {student_id}? (o/n): ")
        
        if confirm.lower() == 'o':
            success = student_service.delete(student_id)
            if success:
                print("Etudiant supprime avec succes!")
            else:
                print("Etudiant introuvable!")
        else:
            print("Suppression annulee")
    except ValueError:
        print("ID invalide!")


def main():
    student_service = StudentService()
    class_service = ClassService()
    
    while True:
        display_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            create_view(student_service, class_service)
        elif choice == "2":
            get_by_id_view(student_service)
        elif choice == "3":
            get_all_view(student_service)
        elif choice == "4":
            get_all_with_class_view(student_service)
        elif choice == "5":
            update_view(student_service, class_service)
        elif choice == "6":
            delete_view(student_service)
        elif choice == "7":
            print("\nAu revoir!")
            break
        else:
            print("Option invalide!")


if __name__ == "__main__":
    main()
