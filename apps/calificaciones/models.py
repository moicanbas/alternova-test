from django.db import models
from apps.accounts.models import CustomUser
from apps.core.models import BaseModel


class Departments(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "calificaciones_department"
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class Student(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    entry_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "calificaciones_student"
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Teacher(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    entry_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(
        Departments, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "calificaciones_teacher"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Period(BaseModel):
    TIPO_CHOICES = [
        ('SE', 'Semestral'),
        ('VA', 'Vacacional'),
    ]
    STATE_CHOICES = [
        ('OPEN', 'ABIERTO'),
        ('END', 'CERRADO'),
    ]
    type = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "calificaciones_period"
        verbose_name = "Period"
        verbose_name_plural = "Periods"

    def __str__(self):
        return f"Periodo {self.id} - {self.type} desde {self.start_date} hasta {self.end_date}"


class Subject(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    credits = models.PositiveIntegerField()

    class Meta:
        db_table = "calificaciones_subject"
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.name} creditos {self.credits}"


class SubjectPrerequisite(BaseModel):
    subject = models.ForeignKey(
        Subject, related_name='subject', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(
        Subject, related_name='prerequisite', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject', 'prerequisite')
        db_table = "calificaciones_subjectprerequisite"
        verbose_name = "subject_prerequisite"
        verbose_name_plural = "subject_prerequisites"

    def __str__(self):
        return f"{self.prerequisito.nombre} es prerrequisito de {self.subject.name}"


class Inscription(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    inscription_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.last_name} {self.student.user.first_name} - {self.subject.name} ({self.period.name})"

    class Meta:
        db_table = "calificaciones_inscription"
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"


class SubjectInscription(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    qualification = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)


class TeacherSubject(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.teacher.user.last_name} {self.teacher.user.first_name} {self.teacher.user.identification}"
