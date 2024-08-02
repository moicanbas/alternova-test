from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import InscriptionSerializer, SubjectInscriptionSerializer, TeacherSubjectSerializer, GradeSubjectInscriptionSerializer
from .models import Inscription, Period, Subject, SubjectPrerequisite, SubjectInscription, Student, TeacherSubject, Teacher
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.core.views import BaseModelView


class InscriptionView(generics.GenericAPIView, mixins.CreateModelMixin):
    model = Inscription
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_teacher:
                return Response({"error": "Debes ser estudiante para realizar esta acción"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                count_credits = 0
                subject_ids = request.data.get('subject', [])
                if not subject_ids:
                    return Response({"error": "No llegaron materias para asociar"}, status=status.HTTP_400_BAD_REQUEST)
                
                subjects = Subject.objects.filter(id__in=subject_ids)
                count_credits = sum(subject.credits for subject in subjects)

                prerequisites = SubjectPrerequisite.objects.filter(
                    subject__in=subjects, is_active = True)
                if prerequisites.exists():
                    list_prerequisite = [
                        f"{prerequisite.prerequisite.name} es prerequisito de {prerequisite.subject.name}" for prerequisite in prerequisites
                    ]
                    return Response({"error": list_prerequisite}, status=status.HTTP_400_BAD_REQUEST)

                if count_credits > 21:
                    return Response({"error": "Usted está superando el número máximo de créditos para asignar este periodo."}, status=status.HTTP_400_BAD_REQUEST)

                inscription = serializer.save(student=user.student)

                for subject in subjects:
                    SubjectInscription.objects.create(
                        subject=subject,
                        inscription=inscription
                    )

                return Response({"message": "Registro almacenado exitosamente"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectApprovalView(generics.GenericAPIView, mixins.ListModelMixin):
    model = SubjectInscription
    serializer_class = SubjectInscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    period_param = openapi.Parameter(
        'period', openapi.IN_QUERY, description="ID del periodo", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[period_param])
    def get(self, request, *args, **kwargs):
        try:
            period_id = request.query_params.get('period')
            student = Student.objects.get(user_id=request.user.id)

            inscriptions = Inscription.objects.filter(
                student=student, period_id__in=period_id, is_active=True)
            if not inscriptions.exists():
                return Response({"error": "No hay inscripciones activas para los periodos proporcionados"}, status=status.HTTP_404_NOT_FOUND)

            list_subjects = []
            for inscription in inscriptions:
                subjects_inscriptions = SubjectInscription.objects.filter(
                    inscription=inscription)
                for sub in subjects_inscriptions:
                    if sub.qualification:
                        if sub.qualification >= 3.0:
                            list_subjects.append({'materia': sub.subject.name, 'cod_materia': sub.subject.code, 'nota': sub.subject.qualification, 'estado': 'aprobado'})
                        else:
                           list_subjects.append({'materia': sub.subject.name, 'cod_materia': sub.subject.code, 'nota': sub.subject.qualification, 'estado': 'reprobado'})
                    else:
                        list_subjects.append({'materia': sub.subject.name, 'cod_materia': sub.subject.code, 'nota': 'N/A', 'estado': 'No registra'})

            
            valid_grades = [sub.qualification for sub in subjects_inscriptions if sub.qualification is not None]

            if valid_grades:
                promedio = sum(valid_grades) / len(valid_grades)
            else:
                promedio = 'N/A'

            return Response({
                "data": {"lista materias": list_subjects, "promedio": promedio }
            }, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectView(generics.GenericAPIView, mixins.ListModelMixin):
    model = SubjectInscription
    serializer_class = SubjectInscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    period_param = openapi.Parameter(
        'period', openapi.IN_QUERY, description="ID del periodo", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[period_param])
    def get(self, request, *args, **kwargs):
        try:
            period_ids = request.query_params.getlist('period')
            student = Student.objects.get(user_id=request.user.id)

            inscriptions = Inscription.objects.filter(
                student=student, period_id__in=period_ids, is_active=True)
            if not inscriptions.exists():
                return Response({"error": "No hay inscripciones activas para los periodos proporcionados"}, status=status.HTTP_404_NOT_FOUND)

            list_subjects = []
            for inscription in inscriptions:
                subjects_inscriptions = SubjectInscription.objects.filter(
                    inscription=inscription)
                list_subjects += [
                    f'{sub.subject.name} - créditos {sub.subject.credits}' for sub in subjects_inscriptions]

            return Response({
                "data": {"lista materias": list_subjects}
            }, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 6. Un profesor puede tener asignadas varias materias
class TeacherSubjectView(BaseModelView):
    model = TeacherSubject
    serializer_class = TeacherSubjectSerializer


# 7. Un profesor puede obtener las lista de materias a las que esta asignado
class TeacherSubjectListView(generics.GenericAPIView, mixins.ListModelMixin):
    model = TeacherSubject
    serializer_class = TeacherSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            if user.is_student:
                return Response({"error": "Debe ser profesor para ejecutar esta acción"}, status=status.HTTP_400_BAD_REQUEST)
            teacher = Teacher.objects.get(user=user)

            subjects = TeacherSubject.objects.get(teacher=teacher)
            list_subjects = [{'Nombre': sub.name, 'Code': sub.code, 'Créditos': sub.credits,
                              'Descripción': sub.description} for sub in subjects.subject.all()]

            return Response({"data": list_subjects}, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 8. Un profesor puede ver la lista de estudiantes de cada una de sus materias
class TeacherStudentsListView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            if user.is_student or not user.is_teacher:
                return Response({"error": "Debe ser profesor para ejecutar esta acción"}, status=status.HTTP_400_BAD_REQUEST)

            teacher = Teacher.objects.get(user=user)
            teacher_subjects = TeacherSubject.objects.filter(teacher=teacher)
            open_periods = Period.objects.filter(state='OPEN')

            if not teacher_subjects or not open_periods:
                return Response({"error": "No hay materias asignadas o períodos activos"}, status=status.HTTP_400_BAD_REQUEST)

            inscriptions = SubjectInscription.objects.filter(
                inscription__period__in=open_periods,
                subject__in=teacher_subjects.values_list('subject', flat=True)
            )

            student_data = []
            for inscription in inscriptions:
                student_data.append({
                    'estudiante': f"{inscription.student.user.last_name} {inscription.student.user.first_name}",
                    'inscripción': inscription.id,
                })

            return Response({"data": student_data}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Period.DoesNotExist:
            return Response({"error": "No hay períodos activos"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 9. Un profesor finaliza la materia (califica cada estudiante)
class GradeStudentView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GradeSubjectInscriptionSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_teacher:
                return Response({"error": "Debe ser profesor para ejecutar esta acción"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                subject_inscription_id = serializer.validated_data.get('id')
                qualification = serializer.validated_data.get('qualification')
                subject = serializer.validated_data.get('subject')
                student = serializer.validated_data.get('student')

                subject_inscription = SubjectInscription.objects.get(
                    id=subject_inscription_id, subject=subject, inscription__student=student)
                teacher = Teacher.objects.get(user=user)
                teacher_subjects = TeacherSubject.objects.filter(
                    teacher=teacher, subject=subject)

                if not teacher_subjects.exists():
                    return Response({"error": "No tienes permiso para calificar esta materia"}, status=status.HTTP_400_BAD_REQUEST)

                subject_inscription.qualification = qualification
                subject_inscription.save()

                return Response({"message": "Calificación registrada exitosamente"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SubjectInscription.DoesNotExist:
            return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 10. Un profesor puede obtener las calificaciones de los estudiantes en sus materias
class StudentGradesView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectInscriptionSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_teacher:
                return Response({"error": "Debe ser profesor para ejecutar esta acción"}, status=status.HTTP_400_BAD_REQUEST)

            teacher = Teacher.objects.get(user=user)
            teacher_subjects = TeacherSubject.objects.filter(teacher=teacher)
            open_periods = Period.objects.filter(state='OPEN')

            if not teacher_subjects or not open_periods.exists():
                return Response({"error": "No hay materias asignadas o períodos activos"}, status=status.HTTP_400_BAD_REQUEST)

            subject_ids = teacher_subjects.values_list('subject', flat=True)
            inscriptions = Inscription.objects.filter(
                period__in=open_periods, subject__in=subject_ids
            )

            grades_data = []
            for inscription in inscriptions:
                for subject_inscription in SubjectInscription.objects.filter(inscription=inscription):
                    grades_data.append({
                        'estudiante': f"{inscription.student.user.last_name} {inscription.student.user.first_name}",
                        'materia': subject_inscription.subject.name,
                        'calificación': subject_inscription.qualification,
                    })

            return Response({"data": grades_data}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Period.DoesNotExist:
            return Response({"error": "No hay períodos activos"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
