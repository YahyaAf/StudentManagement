from src.services.grade_service import GradeService
from src.services.student_service import StudentService
from src.services.subject_service import SubjectService


def display_menu():
    print("\n" + "="*40)
    print("       MENU GRADE")
    print("="*40)
    print("1. Ajouter une note")
    print("2. Afficher notes par etudiant")
    print("3. Afficher tous les etudiants avec notes")
    print("4. Afficher etudiants par matiere")
    print("5. Quitter")
    print("="*40)


def select_student(student_service: StudentService) -> int:
    print("\n--- SELECTIONNER UN ETUDIANT ---")
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


def select_subject(subject_service: SubjectService) -> int:
    print("\n--- SELECTIONNER UNE MATIERE ---")
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


def create_view(grade_service: GradeService, student_service: StudentService, subject_service: SubjectService):
    print("\n--- AJOUTER UNE NOTE ---")
    
    student_id = select_student(student_service)
    if student_id == 0:
        return
    
    subject_id = select_subject(subject_service)
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
        print("Note invalide! Entrer un nombre.")


def get_grades_by_student_view(grade_service: GradeService, student_service: StudentService):
    print("\n--- NOTES PAR ETUDIANT ---")
    
    student_id = select_student(student_service)
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
            print(f"  Date: {g['created_at']}")
            total += g['grade'] * g['coefficient']
            total_coef += g['coefficient']
        
        if total_coef > 0:
            moyenne = total / total_coef
            print(f"\n>>> Moyenne generale: {moyenne:.2f}/20")
    else:
        print("Aucune note trouvee pour cet etudiant")


def get_all_students_with_grades_view(grade_service: GradeService):
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


def get_students_by_subject_view(grade_service: GradeService, subject_service: SubjectService):
    print("\n--- ETUDIANTS PAR MATIERE ---")
    
    subject_id = select_subject(subject_service)
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
            print(f"  Date: {student['created_at']}")
            total_notes += student['grade']
        
        if len(students) > 0:
            moyenne_classe = total_notes / len(students)
            print(f"\n>>> Moyenne de la classe: {moyenne_classe:.2f}/20")
    else:
        print("Aucun etudiant n'a de note pour cette matiere")


def main():
    grade_service = GradeService()
    student_service = StudentService()
    subject_service = SubjectService()
    
    while True:
        display_menu()
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            create_view(grade_service, student_service, subject_service)
        elif choice == "2":
            get_grades_by_student_view(grade_service, student_service)
        elif choice == "3":
            get_all_students_with_grades_view(grade_service)
        elif choice == "4":
            get_students_by_subject_view(grade_service, subject_service)
        elif choice == "5":
            print("\nAu revoir!")
            break
        else:
            print("Option invalide!")


if __name__ == "__main__":
    main()
