from rest_framework import serializers
from apps.calificaciones.models import Period, Departments, Student, Teacher, Subject, TeacherSubject, SubjectPrerequisite


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'type', 'start_date', 'end_date']


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'name', 'description']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'credits']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user_id', 'user', 'birth_date', 'entry_date']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user_id', 'user', 'department']


class SubjectPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectPrerequisite
        fields = ['subject', 'prerequisite']