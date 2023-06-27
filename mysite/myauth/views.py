from random import random
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from django.utils.translation import gettext_lazy as _, ngettext
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.forms import UserCreationForm

from myauth.forms import AvatarForm
from myauth.models import Profile
import logging

class HelloView(View):
    welcome_message = _('welcome hello world!')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f'<h1>{self.welcome_message}</h1>'
            f'<h2>{products_line}</h1>'
        )


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    context_object_name = 'profile'

    def post(self, request, *args, **kwargs):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('myauth:about-me')
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AvatarForm()
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


@login_required
def avatar_upload(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('myauth:about-me')
    else:
        form = AvatarForm()
    return render(request, 'myauth/avatar_upload.html', {'form': form})


@login_required
def users_list_view(request):
    users = User.objects.all()
    return render(request, 'myauth/users_list.html', {'users': users})


@login_required
def user_detail_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'myauth/user_details.html', {'user': user})


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True
    logger = logging.getLogger('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.logger.info('Пользователь вошел в систему')
        return response


def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error': 'Invalid username or password'})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')
    logger = logging.getLogger('logout')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        self.logger.info('Пользователь вышел из системы')
        return response


class CustomLogoutView(LogoutView):
    next_page = '/'  # изменение страницы для перенаправления пользователя

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page == self.next_page:
            return next_page
        else:
            return self.next_page


# @user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r} + {random()}')


@permission_required('view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
