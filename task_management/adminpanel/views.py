import logging
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from authentication.models import User
from tasks.models import Task

logger = logging.getLogger(__name__)

class LoginView(View):
    def get(self, request):
        return render(request, 'adminpanel/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.role in ['admin', 'superadmin']:
            print("k")
            login(request, user)
            logger.info(f"User {user.username} logged in to admin panel")
            return redirect('admin_dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials or not authorized'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('admin_login')

class DashboardView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def get(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return redirect('admin_login')
        return render(request, 'adminpanel/dashboard.html')

class UserListView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def get(self, request):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        users = User.objects.all()
        admins = User.objects.filter(role='admin')
        return render(request, 'adminpanel/user_list.html', {'users': users, 'admins': admins})

class CreateUserView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def get(self, request):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        return render(request, 'adminpanel/create_user.html')

    def post(self, request):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        role = request.POST.get('role', 'user')
        if role not in ['user', 'admin']:
            role = 'user'
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        logger.info(f"User {user.username} created by {request.user.username}")
        return redirect('user_list')

class DeleteUserView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def post(self, request, pk):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        user = get_object_or_404(User, pk=pk)
        if user.role == 'superadmin':
            return HttpResponseForbidden('Cannot delete superadmin')
        username = user.username
        user.delete()
        logger.info(f"User {username} deleted by {request.user.username}")
        return redirect('user_list')

class UpdateRoleView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def post(self, request, pk):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        user = get_object_or_404(User, pk=pk)
        new_role = request.POST.get('new_role')
        if new_role in ['user', 'admin', 'superadmin']:
            old_role = user.role
            user.role = new_role
            user.save()
            logger.info(f"User {user.username} role updated from {old_role} to {new_role} by {request.user.username}")
        return redirect('user_list')

class AssignUserToAdminView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def post(self, request):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        user_id = request.POST.get('user_id')
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(User, id=user_id, role='user')
        admin = get_object_or_404(User, id=admin_id, role='admin')
        user.assigned_to = admin
        user.save()
        logger.info(f"User {user.username} assigned to {admin.username} by {request.user.username}")
        return redirect('user_list')

class TaskListView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def get(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return redirect('admin_dashboard')
        if request.user.role == 'superadmin':
            tasks = Task.objects.all()
        else:
            users = request.user.assigned_users.all()
            tasks = Task.objects.filter(assigned_to__in=users)
        return render(request, 'adminpanel/task_list.html', {'tasks': tasks})

class CreateTaskView(LoginRequiredMixin, View):
    login_url = '/adminpanel/login/'
    def get(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return redirect('admin_dashboard')
        if request.user.role == 'superadmin':
            users = User.objects.filter(role='user')
        else:
            users = request.user.assigned_users.all()
        return render(request, 'adminpanel/create_task.html', {'users': users})

    def post(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return redirect('admin_dashboard')
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        if request.user.role == 'superadmin':
            assigned_to = get_object_or_404(User, id=assigned_to_id, role='user')
        else:
            assigned_to = get_object_or_404(User, id=assigned_to_id, assigned_to=request.user, role='user')
        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
        )
        logger.info(f"Task {task.title} created and assigned to {assigned_to.username} by {request.user.username}")
        return redirect('task_list')

