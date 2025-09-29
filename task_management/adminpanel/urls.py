from django.urls import path
from .views import (
    LoginView, LogoutView, DashboardView, CreateUserView, UserListView,
    DeleteUserView, UpdateRoleView, AssignUserToAdminView, CreateTaskView,
    TaskListView, UpdateTaskView, DeleteTaskView, TaskReportAdminView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),
    path('dashboard/', DashboardView.as_view(), name='admin_dashboard'),
]