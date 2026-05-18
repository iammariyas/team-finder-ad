from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    LoginForm,
    ProfileEditForm,
    RegisterForm,
)
from .models import User
from .pagination import paginate

USER_FILTER_OWNERS_OF_FAVORITE = 'owners-of-favorite-projects'
USER_FILTER_OWNERS_OF_PARTICIPATING = 'owners-of-participating-projects'
USER_FILTER_INTERESTED_IN_MY = 'interested-in-my-projects'
USER_FILTER_PARTICIPANTS_OF_MY = 'participants-of-my-projects'

VALID_USER_FILTERS = frozenset(
    {
        USER_FILTER_OWNERS_OF_FAVORITE,
        USER_FILTER_OWNERS_OF_PARTICIPATING,
        USER_FILTER_INTERESTED_IN_MY,
        USER_FILTER_PARTICIPANTS_OF_MY,
    }
)


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        phone = data['phone']
        User.objects.create_user(
            data['email'],
            data['name'],
            data['surname'],
            password=data['password'],
            phone=phone,
        )
        messages.success(
            request,
            'Регистрация прошла успешно. Войдите в систему, используя email и пароль.',
        )
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('project_list')
        form.add_error(None, 'Неверный email или пароль')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('project_list')


def user_list(request):
    qs = User.objects.all()
    raw_filter = (request.GET.get('filter') or '').strip()
    query_prefix = ''
    active_filter = None

    if request.user.is_authenticated and raw_filter in VALID_USER_FILTERS:
        active_filter = raw_filter
        u = request.user
        if active_filter == USER_FILTER_OWNERS_OF_FAVORITE:
            qs = User.objects.filter(
                id__in=u.favorites.values_list('owner_id', flat=True)
            ).distinct()
        elif active_filter == USER_FILTER_OWNERS_OF_PARTICIPATING:
            qs = User.objects.filter(
                id__in=u.participated_projects.values_list('owner_id', flat=True)
            ).distinct()
        elif active_filter == USER_FILTER_INTERESTED_IN_MY:
            qs = User.objects.filter(
                favorites__in=u.owned_projects.all()
            ).distinct()
        elif active_filter == USER_FILTER_PARTICIPANTS_OF_MY:
            qs = User.objects.filter(
                participated_projects__in=u.owned_projects.all()
            ).distinct()
        query_prefix = urlencode({'filter': active_filter}) + '&'

    page_obj = paginate(request, qs)
    return render(
        request,
        'users/participants.html',
        {'page_obj': page_obj, 'active_filter': active_filter, 'query_prefix': query_prefix},
    )


def user_detail(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': profile_user})


@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('users:user_detail', user_id=request.user.pk)
    return render(
        request,
        'users/edit_profile.html',
        {'form': form, 'user': request.user},
    )


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Пароль успешно изменён.')
        return redirect('users:user_detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})
