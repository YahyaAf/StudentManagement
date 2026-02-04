from src.services.user_service import UserService
from src.services.class_service import ClassService
from src.services.student_service import StudentService
from src.services.subject_service import SubjectService
from src.services.grade_service import GradeService
from datetime import date


user_service = UserService()
class_service = ClassService()
student_service = StudentService()
subject_service = SubjectService()
grade_service = GradeService()


def display_login_menu():
    print("\n" + "="*50)
    print("       SYSTEME DE GESTION SCOLAIRE")
    print("="*50)
    print("1. Login")
    print("2. Quitter")
    print("="*50)


def login_view():
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")
    
    success = user_service.login(username, password)
    
    if success:
        print(f"\nConnecte avec succes!")
        print(f"Bienvenue {user_service.current_user.username} ({user_service.current_user.role})")
        return True
    else:
        print("\nUsername ou password incorrect!")
        return False


def display_admin_menu():
    print("\n" + "="*50)
    print(f"       MENU ADMIN - {user_service.current_user.username}")
    print("="*50)
    print("--- GESTION USERS ---")
    print("1. Register un nouvel utilisateur")
    print("2. Afficher utilisateur actuel")
    print("\n--- GESTION CLASSES ---")
    print("3. Creer une classe")
    print("4. Afficher toutes les classes")
    print("5. Modifier une classe")
    print("6. Supprimer une classe")
    print("\n--- GESTION ETUDIANTS ---")
    print("7. Creer un etudiant")
    print("8. Afficher tous les etudiants")
    print("9. Afficher etudiants avec classes")
    print("10. Modifier un etudiant")
    print("11. Supprimer un etudiant")
    print("\n--- GESTION MATIERES ---")
    print("12. Creer une matiere")
    print("13. Afficher toutes les matieres")
    print("14. Modifier une matiere")
    print("15. Supprimer une matiere")
    print("\n--- GESTION NOTES ---")
    print("16. Ajouter une note")
    print("17. Afficher notes par etudiant")
    print("18. Afficher tous etudiants avec notes")
    print("19. Afficher etudiants par matiere")
    print("\n20. Logout")
    print("="*50)


def display_staff_menu():
    print("\n" + "="*50)
    print(f"       MENU STAFF - {user_service.current_user.username}")
    print("="*50)
    print("1. Afficher utilisateur actuel")
    print("\n--- AFFICHAGE ---")
    print("2. Afficher toutes les classes")
    print("3. Afficher tous les etudiants")
    print("4. Afficher etudiants avec classes")
    print("5. Afficher toutes les matieres")
    print("\n--- GESTION NOTES ---")
    print("6. Ajouter une note")
    print("7. Afficher notes par etudiant")
    print("8. Afficher tous etudiants avec notes")
    print("9. Afficher etudiants par matiere")
    print("\n10. Logout")
    print("="*50)


def register_view():
    print("\n--- REGISTER NOUVEL UTILISATEUR ---")
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (admin/staff) [staff]: ") or "staff"
    
    user = user_service.register(username, password, role)
    
    if user:
        print(f"User cree avec succes: {user}")
    else:
        print("Erreur: Username deja existant!")


def me_view():
    print("\n--- UTILISATEUR ACTUEL ---")
    user = user_service.me()
    
    if user:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")
        print(f"Created at: {user.created_at}")
        print(f"Status: Connecte")
    else:
        print("Aucun utilisateur connecte")


def create_class_view():
    print("\n--- CREER UNE CLASSE ---")
    name = input("Nom: ")
    level = input("Niveau: ")
    year = input("Annee: ")
    
    class_obj = class_service.create(name, level, year)
    
    if class_obj:
        print(f"Classe creee avec succes: {class_obj}")
    else:
        print("Erreur lors de la creation!")


def get_all_classes_view():
    print("\n--- LISTE DES CLASSES ---")
    classes = class_service.get_all()
    
    if classes:
        for class_obj in classes:
            print(f"- {class_obj}")
    else:
        print("Aucune classe trouvee")


def update_class_view():
    print("\n--- MODIFIER UNE CLASSE ---")
    class_id = input("ID de la classe: ")
    
    try:
        class_id = int(class_id)
        class_obj = class_service.get_by_id(class_id)
        
        if not class_obj:
            print("Classe introuvable!")
            return
        
        print(f"Classe actuelle: {class_obj}")
        name = input("Nouveau nom (vide pour garder): ")
        level = input("Nouveau niveau (vide pour garder): ")
        year = input("Nouvelle annee (vide pour garder): ")
        
        success = class_service.update(
            class_id,
            name if name else None,
            level if level else None,
            year if year else None
        )
        
        if success:
            print("Classe modifiee avec succes!")
    except ValueError:
        print("ID invalide!")


def delete_class_view():
    print("\n--- SUPPRIMER UNE CLASSE ---")
    class_id = input("ID de la classe: ")
    
    try:
        class_id = int(class_id)
        confirm = input(f"Confirmer la suppression de la classe {class_id}? (o/n): ")
        
        if confirm.lower() == 'o':
            success = class_service.delete(class_id)
            if success:
                print("Classe supprimee avec succes!")
            else:
                print("Classe introuvable!")
    except ValueError:
        print("ID invalide!")


def select_class() -> int:
    classes = class_service.get_all()
    
    if not classes:
        print("Aucune classe disponible!")
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
                print("ID invalide!")
        except ValueError:
            print("Entrer un numero valide!")


def create_student_view():
    print("\n--- CREER UN ETUDIANT ---")
    
    class_id = select_class()
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
            print("Erreur lors de la creation!")
    except ValueError:
        print("Date invalide! Format: YYYY-MM-DD")


def get_all_students_view():
    print("\n--- LISTE DES ETUDIANTS ---")
    students = student_service.get_all()
    
    if students:
        for student in students:
            print(f"- {student}")
    else:
        print("Aucun etudiant trouve")


def get_all_students_with_class_view():
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
        print("Aucun etudiant trouve")


def update_student_view():
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
        
        change_class = input("Changer de classe? (o/n): ")
        class_id = None
        if change_class.lower() == 'o':
            class_id = select_class()
            if class_id == 0:
                class_id = None
        
        success = student_service.update(
            student_id,
            first_name if first_name else None,
            last_name if last_name else None,
            email if email else None,
            phone if phone else None,
            None,
            class_id
        )
        
        if success:
            print("Etudiant modifie avec succes!")
    except ValueError:
        print("ID invalide!")


def delete_student_view():
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
    except ValueError:
        print("ID invalide!")


def create_subject_view():
    print("\n--- CREER UNE MATIERE ---")
    name = input("Nom: ")
    coefficient = input("Coefficient: ")
    
    try:
        coefficient = float(coefficient)
        subject = subject_service.create(name, coefficient)
        
        if subject:
            print(f"Matiere creee avec succes: {subject}")
        else:
            print("Erreur lors de la creation!")
    except ValueError:
        print("Coefficient invalide!")


def get_all_subjects_view():
    print("\n--- LISTE DES MATIERES ---")
    subjects = subject_service.get_all()
    
    if subjects:
        for subject in subjects:
            print(f"- {subject}")
    else:
        print("Aucune matiere trouvee")


def update_subject_view():
    print("\n--- MODIFIER UNE MATIERE ---")
    subject_id = input("ID de la matiere: ")
    
    try:
        subject_id = int(subject_id)
        subject = subject_service.get_by_id(subject_id)
        
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
        
        success = subject_service.update(subject_id, name if name else None, coefficient)
        
        if success:
            print("Matiere modifiee avec succes!")
    except ValueError:
        print("ID invalide!")


def delete_subject_view():
    print("\n--- SUPPRIMER UNE MATIERE ---")
    subject_id = input("ID de la matiere: ")
    
    try:
        subject_id = int(subject_id)
        confirm = input(f"Confirmer la suppression de la matiere {subject_id}? (o/n): ")
        
        if confirm.lower() == 'o':
            success = subject_service.delete(subject_id)
            if success:
                print("Matiere supprimee avec succes!")
            else:
                print("Matiere introuvable!")
    except ValueError:
        print("ID invalide!")


def select_student() -> int:
    students = student_service.get_all()
    
    if not students:
        print("Aucun etudiant disponible!")
        return 0
    
    print("\nEtudiants disponibles:")
    for student in students:
        print(f"{student.id}. {student.first_name} {student.last_name} - {student.email}")
    
    while True:
        try:
            student_id = int(input("\nChoisir l'ID de l'etudiant: "))
            if any(s.id == student_id for s in students):
                return student_id
            else:
                print("ID invalide!")
        except ValueError:
            print("Entrer un numero valide!")


def select_subject() -> int:
    subjects = subject_service.get_all()
    
    if not subjects:
        print("Aucune matiere disponible!")
        return 0
    
    print("\nMatieres disponibles:")
    for subject in subjects:
        print(f"{subject.id}. {subject.name} - Coefficient: {subject.coefficient}")
    
    while True:
        try:
            subject_id = int(input("\nChoisir l'ID de la matiere: "))
            if any(s.id == subject_id for s in subjects):
                return subject_id
            else:
                print("ID invalide!")
        except ValueError:
            print("Entrer un numero valide!")


def create_grade_view():
    print("\n--- AJOUTER UNE NOTE ---")
    
    student_id = select_student()
    if student_id == 0:
        return
    
    subject_id = select_subject()
    if subject_id == 0:
        return
    
    grade_value = input("Note (0-20): ")
    
    try:
        grade_value = float(grade_value)
        if grade_value < 0 or grade_value > 20:
            print("La note doit etre entre 0 et 20!")
            return
        
        grade = grade_service.create(student_id, subject_id, grade_value)
        
        if grade:
            print(f"Note ajoutee avec succes: {grade}")
        else:
            print("Erreur lors de l'ajout de la note!")
    except ValueError:
        print("Note invalide!")


def get_grades_by_student_view():
    print("\n--- NOTES PAR ETUDIANT ---")
    
    student_id = select_student()
    if student_id == 0:
        return
    
    grades = grade_service.get_grades_by_student(student_id)
    
    if grades:
        print(f"\n=== Notes de {grades[0]['student_name']} ({grades[0]['student_email']}) ===")
        total = 0
        total_coef = 0
        for g in grades:
            print(f"\n- Matiere: {g['subject_name']}")
            print(f"  Note: {g['grade']}/20")
            print(f"  Coefficient: {g['coefficient']}")
            total += g['grade'] * g['coefficient']
            total_coef += g['coefficient']
        
        if total_coef > 0:
            moyenne = total / total_coef
            print(f"\n>>> Moyenne generale: {moyenne:.2f}/20")
    else:
        print("Aucune note trouvee")


def get_all_students_with_grades_view():
    print("\n--- TOUS LES ETUDIANTS AVEC NOTES ---")
    
    students = grade_service.get_all_students_with_grades()
    
    if students:
        for student in students:
            print(f"\n{'='*60}")
            print(f"Etudiant: {student['student_name']} ({student['email']})")
            if student['class_name']:
                print(f"Classe: {student['class_name']} - {student['class_level']}")
            
            if student['grades']:
                print("\nNotes:")
                total = 0
                total_coef = 0
                for grade in student['grades']:
                    print(f"  - {grade['subject_name']}: {grade['grade']}/20 (Coef: {grade['coefficient']})")
                    total += grade['grade'] * grade['coefficient']
                    total_coef += grade['coefficient']
                
                if total_coef > 0:
                    moyenne = total / total_coef
                    print(f"\n  >>> Moyenne: {moyenne:.2f}/20")
            else:
                print("Aucune note")
    else:
        print("Aucun etudiant trouve")


def get_students_by_subject_view():
    print("\n--- ETUDIANTS PAR MATIERE ---")
    
    subject_id = select_subject()
    if subject_id == 0:
        return
    
    students = grade_service.get_students_by_subject(subject_id)
    
    if students:
        print(f"\n=== Matiere: {students[0]['subject_name']} (Coefficient: {students[0]['coefficient']}) ===")
        print(f"\nNombre d'etudiants: {len(students)}")
        
        total_notes = 0
        for student in students:
            print(f"\n- {student['student_name']} ({student['student_email']})")
            if student['class_name']:
                print(f"  Classe: {student['class_name']}")
            print(f"  Note: {student['grade']}/20")
            total_notes += student['grade']
        
        if len(students) > 0:
            moyenne_classe = total_notes / len(students)
            print(f"\n>>> Moyenne de la classe: {moyenne_classe:.2f}/20")
    else:
        print("Aucun etudiant n'a de note pour cette matiere")


def admin_menu():
    while user_service.is_logged_in:
        display_admin_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            register_view()
        elif choice == "2":
            me_view()
        elif choice == "3":
            create_class_view()
        elif choice == "4":
            get_all_classes_view()
        elif choice == "5":
            update_class_view()
        elif choice == "6":
            delete_class_view()
        elif choice == "7":
            create_student_view()
        elif choice == "8":
            get_all_students_view()
        elif choice == "9":
            get_all_students_with_class_view()
        elif choice == "10":
            update_student_view()
        elif choice == "11":
            delete_student_view()
        elif choice == "12":
            create_subject_view()
        elif choice == "13":
            get_all_subjects_view()
        elif choice == "14":
            update_subject_view()
        elif choice == "15":
            delete_subject_view()
        elif choice == "16":
            create_grade_view()
        elif choice == "17":
            get_grades_by_student_view()
        elif choice == "18":
            get_all_students_with_grades_view()
        elif choice == "19":
            get_students_by_subject_view()
        elif choice == "20":
            user_service.logout()
            print("\nDeconnecte avec succes!")
        else:
            print("Option invalide!")


def staff_menu():
    while user_service.is_logged_in:
        display_staff_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            me_view()
        elif choice == "2":
            get_all_classes_view()
        elif choice == "3":
            get_all_students_view()
        elif choice == "4":
            get_all_students_with_class_view()
        elif choice == "5":
            get_all_subjects_view()
        elif choice == "6":
            create_grade_view()
        elif choice == "7":
            get_grades_by_student_view()
        elif choice == "8":
            get_all_students_with_grades_view()
        elif choice == "9":
            get_students_by_subject_view()
        elif choice == "10":
            user_service.logout()
            print("\nDeconnecte avec succes!")
        else:
            print("Option invalide!")


def main():
    print("\n*** SYSTEME DE GESTION SCOLAIRE ***")
    
    while True:
        if not user_service.is_logged_in:
            display_login_menu()
            choice = input("\nChoisissez une option: ")
            
            if choice == "1":
                if login_view():
                    if user_service.current_user.role == "admin":
                        admin_menu()
                    elif user_service.current_user.role == "staff":
                        staff_menu()
            elif choice == "2":
                print("\nAu revoir!")
                break
            else:
                print("Option invalide!")
        else:
            if user_service.current_user.role == "admin":
                admin_menu()
            elif user_service.current_user.role == "staff":
                staff_menu()


if __name__ == "__main__":
    main()
    main()
