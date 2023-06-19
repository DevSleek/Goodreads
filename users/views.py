from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import UserCreateForm, UserUpdateFrom
from django.views import View


class RegisterView(View):
    @staticmethod
    def get(request):
        form = UserCreateForm()
        context = {
            'form': form
        }

        return render(request, 'users/register.html', context)

    @staticmethod
    def post(request):
        form = UserCreateForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')
        
        else:
            context = {
                'form': form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    @staticmethod
    def get(request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'users/login.html', context)

    @staticmethod
    def post(request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')

            return redirect('books:books-list')

        else:
            context = {
                'login_form': login_form
            }
            return render(request, 'users/login.html', context)


class ProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        user = request.user
        return render(request, 'users/profile.html', {'user': user})


class LogoutView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        messages.info(request, 'You have successfully logged out.')
        return redirect('landing_page')


class ProfileUpdateView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        update_form = UserUpdateFrom(instance=request.user)

        context = {
            'update_form': update_form
        }
        return render(request, 'users/profile_edit.html', context)

    @staticmethod
    def post(request):
        update_form = UserUpdateFrom(instance=request.user, data=request.POST, files=request.FILES)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'You have successfully updated your profile.')
            return redirect('users:profile')

        return render(request, 'users/profile_edit.html', {'update_form': update_form})
