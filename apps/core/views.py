from rest_framework import status
from django.core.exceptions import ValidationError
from apps.calificaciones.models import Period, Departments, Student, Teacher, Subject, TeacherSubject, SubjectPrerequisite
from .serializers import (PeriodSerializer, DepartmentsSerializer, StudentSerializer,
                          TeacherSerializer, SubjectSerializer, SubjectPrerequisiteSerializer)
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

class BaseModelView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    model = None
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        try:
            if 'pk' in kwargs:
                instance = self.get_object()
                serializer = self.serializer_class(instance)
                return Response({
                    "success": True,
                    "count": 1,
                    "results": serializer.data
                })
            else:
                queryset = self.get_queryset()
                serializer = self.serializer_class(queryset, many=True)
                return Response({
                    "success": True,
                    "count": len(serializer.data),
                    "results": serializer.data
                })
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                is_teacher = request.data.get('is_teacher', None)
                is_student = request.data.get('is_student', None)
                
                instance = serializer.save()
                if is_teacher:
                    Teacher.objects.create(user = instance)

                elif is_student:
                    Teacher.objects.create(user = instance)
                    
                return Response({"message": "Registro almacenado exitosamente"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            if 'pk' not in kwargs:
                return Response({"error": "Method PUT not allowed without a pk"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            instance = self.get_object()
            serializer = self.serializer_class(
                instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Registro actualizado exitosamente"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            if 'pk' not in kwargs:
                return Response({"error": "Method DELETE not allowed without a pk"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            instance = self.get_object()
            if not instance.is_active:
                return Response({"error": "No se encontró registro con este ID"}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_active = False
            instance.save()
            return Response({"message": "Registro eliminado exitosamente"}, status=status.HTTP_204_NO_CONTENT)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PeriodView(BaseModelView):
    model = Period
    serializer_class = PeriodSerializer


class DepartmentsView(BaseModelView):
    model = Departments
    serializer_class = DepartmentsSerializer


class StudentView(BaseModelView):
    model = Student
    serializer_class = StudentSerializer


class TeacherView(BaseModelView):
    model = Teacher
    serializer_class = TeacherSerializer


class SubjectView(BaseModelView):
    model = Subject
    serializer_class = SubjectSerializer

class SubjectPrerequisiteView(BaseModelView):
    model = SubjectPrerequisite
    serializer_class = SubjectPrerequisiteSerializer

