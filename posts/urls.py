from .import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        next_page='/',
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
]