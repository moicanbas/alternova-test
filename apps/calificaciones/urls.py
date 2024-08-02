from django.urls import path
from .views import (
    InscriptionView, SubjectApprovalView, SubjectView, TeacherSubjectView,
    TeacherSubjectListView, TeacherStudentsListView, GradeStudentView, StudentGradesView
)

app_name = 'calificaciones'

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription-list'),
    # path('inscription/<int:pk>/', InscriptionView.as_view(), name='inscription-detail'),

    path('subjects-approval-list/', SubjectApprovalView.as_view(),
         name='subjects-approval-list'),
    path('subjects-list/', SubjectView.as_view(), name='subjects-list'),

    path('teacher-subject/', TeacherSubjectView.as_view(),
         name='teacher-subject-list'),
    path('teacher-subject/<int:pk>/', TeacherSubjectView.as_view(),
         name='teacher-subject-detail'),
    path('teacher-subject-list/', TeacherSubjectListView.as_view(),
         name='teacher-subject-list'),
    path('teacher-student-list/', TeacherStudentsListView.as_view(),
         name='teacher-student-list'),

    # Nuevas URLs
    path('grade-student/', GradeStudentView.as_view(), name='grade-student'),
    path('student-grades/', StudentGradesView.as_view(), name='student-grades'),
]
