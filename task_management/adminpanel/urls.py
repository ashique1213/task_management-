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
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
   
]