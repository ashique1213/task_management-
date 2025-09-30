import logging
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from authentication.models import User
from tasks.models import Task
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


logger = logging.getLogger(__name__)

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.role in ['admin', 'superadmin']:
            return redirect('admin_dashboard')
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

@method_decorator(never_cache, name='dispatch')
class DashboardView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return redirect('admin_login')
        return render(request, 'adminpanel/dashboard.html')

@method_decorator(never_cache, name='dispatch')
class UserListView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        if request.user.role != 'superadmin':
            return redirect('admin_dashboard')
        users = User.objects.all()
        admins = User.objects.filter(role='admin')
        return render(request, 'adminpanel/user_list.html', {'users': users, 'admins': admins})

class CreateUserView(LoginRequiredMixin, View):
    login_url = '/'
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
    login_url = '/'
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
    login_url = '/'
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
    login_url = '/'
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

@method_decorator(never_cache, name='dispatch')
class TaskListView(LoginRequiredMixin, View):
    login_url = '/'
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
    login_url = '/'
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

class UpdateTaskView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user = request.user
        if user.role == 'superadmin':
            pass
        elif user.role == 'admin':
            if task.assigned_to.assigned_to != user:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        return render(request, 'adminpanel/update_task.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user = request.user
        if user.role == 'superadmin':
            pass
        elif user.role == 'admin':
            if task.assigned_to.assigned_to != user:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        previous_status = task.status
        error = None
        if status == 'Completed':
            completion_report = request.POST.get('completion_report')
            worked_hours = request.POST.get('worked_hours')
            if previous_status != 'Completed':
                if not completion_report or not worked_hours:
                    error = "Completion report and worked hours are required when marking as completed"
            if error:
                return render(request, 'adminpanel/update_task.html', {'task': task, 'error': error})
            if completion_report:
                task.completion_report = completion_report
            if worked_hours:
                try:
                    task.worked_hours = float(worked_hours)
                except ValueError:
                    error = "Worked hours must be a number"
                    return render(request, 'adminpanel/update_task.html', {'task': task, 'error': error})
        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status
        task.save()
        logger.info(f"Task {task.title} updated by {request.user.username}")
        return redirect('task_list')

class DeleteTaskView(LoginRequiredMixin, View):
    login_url = '/'
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user = request.user
        if user.role == 'superadmin':
            pass
        elif user.role == 'admin':
            if task.assigned_to.assigned_to != user:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        title = task.title
        task.delete()
        logger.info(f"Task {title} deleted by {request.user.username}")
        return redirect('task_list')

class TaskReportAdminView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.status != 'Completed':
            return HttpResponseForbidden('Task is not completed')
        user = request.user
        if user.role == 'superadmin':
            pass
        elif user.role == 'admin':
            if task.assigned_to.assigned_to != user:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        logger.info(f"Task {task.id} report viewed in panel by {request.user.username}")
        return render(request, 'adminpanel/task_report.html', {'task': task})