from django.urls import path
from django.contrib.auth.views import LoginView

from myauth.views import (
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    avatar_upload,
    users_list_view,
    # UsersListView,
    # UserDetailsView,
    user_detail_view,
    # UpdateUserProfile,
    HelloView,
    MyLoginView,
)

app_name = 'myauth'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name = 'login'),
    # path('login/', LoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True,),name='login'),
    path('hello/', HelloView.as_view(), name='hello'),
    # path('logout/', logout_view, name='logout'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
    path('avatar-upload/', avatar_upload, name='avatar-upload'),
    # path('users-list/', UsersListView.as_view(), name='users-list'),
    # path('<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path('users/', users_list_view, name='users_list'),
    path('user/<str:username>/', user_detail_view, name='user_details'),
    # path('avatar-upload/', UpdateUserProfile.as_view(), name='avatar-upload'),
]
