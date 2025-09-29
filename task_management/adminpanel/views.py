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

