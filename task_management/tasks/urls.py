from django.urls import path, include
from tasks.views import TaskListView,TaskUpdateView,TaskReportView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
]