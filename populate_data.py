import os
import django
import random
from datetime import date, timedelta
from faker import Faker

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alternova.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.calificaciones.models import Departments, Student, Teacher, Period, Subject, SubjectPrerequisite, Inscription, SubjectInscription, TeacherSubject

# Inicializar Faker para generar datos ficticios
faker = Faker()

def clear_data():
    """Vaciar las tablas antes de llenar con datos ficticios."""
    SubjectInscription.objects.all().delete()
    Inscription.objects.all().delete()
    SubjectPrerequisite.objects.all().delete()
    TeacherSubject.objects.all().delete()
    Subject.objects.all().delete()
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    CustomUser.objects.all().delete()
    Departments.objects.all().delete()
    Period.objects.all().delete()

def create_users(n):
    for i in range(n):
        CustomUser.objects.create_user(
            username=faker.unique.user_name(),
            email=faker.unique.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            password='test1234',
            is_teacher = i > 1,
            is_student = i < 1 
        )
    print('Finalizado users')

def create_departments(n):
    for _ in range(n):
        Departments.objects.create(
            name=faker.unique.word(),
            description=faker.text()
        )
    print('Finalizado departments')

def create_students():
    users = CustomUser.objects.all()
    for user in users:
        if not hasattr(user, 'student'):
            Student.objects.create(
                user=user,
                entry_date=faker.date_between(start_date='-5y', end_date='today'),
                birth_date=faker.date_of_birth(minimum_age=18, maximum_age=30)
            )
    print('Finalizado students')

def create_teachers():
    students = Student.objects.all()
    departments = Departments.objects.all()
    for student in students:
        department = random.choice(departments)
        Teacher.objects.create(
            user=student.user,
            department=department
        )
        
    print('Finalizado teachers')

def create_periods():
    Period.objects.create(
        type='SE',
        state='OPEN',
        start_date=date.today() - timedelta(days=30),
        end_date=date.today() + timedelta(days=150)
    )
    Period.objects.create(
        type='VA',
        state='END',
        start_date=date.today() - timedelta(days=200),
        end_date=date.today() - timedelta(days=100)
    )
    print('Finalizado period')

def create_subjects(n):
    for _ in range(n):
        Subject.objects.create(
            name=faker.unique.word(),
            code=faker.unique.random_number(digits=4),
            description=faker.text(),
            credits=random.randint(1, 5)
        )

def create_prerequisites():
    subjects = Subject.objects.all()
    for subject in subjects:
        prerequisites = random.sample(list(subjects.exclude(id=subject.id)), k=random.randint(0, 3))
        for prerequisite in prerequisites:
            SubjectPrerequisite.objects.create(
                subject=subject,
                prerequisite=prerequisite
            )
    
    print('Finalizado pre')

def create_teacher_subjects():
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    for teacher in teachers:
        teacher_subject = TeacherSubject.objects.create(teacher=teacher)
        teacher_subject.subject.set(random.sample(list(subjects), k=random.randint(1, 3)))

    print('Finalizado otro')
    
# Ejecutar funciones para crear datos ficticios
#clear_data()
create_users(2)
create_departments(3)
create_students()
create_teachers()
create_periods()
create_subjects(5)
create_prerequisites()
create_teacher_subjects()

print("Datos ficticios creados con éxito.")
