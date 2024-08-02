from django.urls import path
from .views import PeriodView, DepartmentsView, SubjectView

app_name = 'core'

urlpatterns = [
    path('period/', PeriodView.as_view(), name='period-list'),
    path('period/<int:pk>/', PeriodView.as_view(), name='period-detail'),

    path('department/', DepartmentsView.as_view(), name='department-list'),
    path('department/<int:pk>/', DepartmentsView.as_view(),
         name='department-detail'),

    path('subject/', SubjectView.as_view(), name='subject-list'),
    path('subject/<int:pk>/', SubjectView.as_view(), name='subject-detail'),
]
