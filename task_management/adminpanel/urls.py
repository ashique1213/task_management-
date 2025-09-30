from django.urls import path
from .views import (
    LoginView, LogoutView, DashboardView, CreateUserView, UserListView,
    DeleteUserView, UpdateRoleView, AssignUserToAdminView, CreateTaskView,
    TaskListView, UpdateTaskView, DeleteTaskView, TaskReportAdminView
)

urlpatterns = [
    path('', LoginView.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),
    path('dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('users/<int:pk>/update_role/', UpdateRoleView.as_view(), name='update_role'),
    path('assign_user/', AssignUserToAdminView.as_view(), name='assign_user'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', CreateTaskView.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/report/', TaskReportAdminView.as_view(), name='task_report'),
]