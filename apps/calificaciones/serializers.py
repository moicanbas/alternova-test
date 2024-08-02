from rest_framework import serializers
from apps.calificaciones.models import Inscription, SubjectInscription, TeacherSubject, Subject, Student


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ('id','inscription_date', 'period')


class SubjectInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectInscription
        fields = ('inscription', 'subject')


class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject']
        

class GradeSubjectInscriptionSerializer(serializers.ModelSerializer):
    qualification = serializers.FloatField(required=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.filter(is_active = True))
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.filter(is_active = True))

    class Meta:
        model = SubjectInscription
        fields = ('id', 'qualification', 'subject', 'student')


