from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact', views.contact, name='contact'),
    path('add_task', views.add_task, name='add_task'),
    path('change_status/<int:id>/', views.change_status, name='change_status'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('update_task/<int:id>/', views.update_task, name='update_taask'),

    path('user_register/', views.user_register, name="user_register"),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),

    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/password_reset/', name='password_reset'),
    # path('accounts/password_change/', name='password_change'),
    # path('accounts/password_change/done/', name='password_change_done'),
    # path('accounts/password_reset/', name='password_reset'),
    # path('accounts/password_reset/done/', name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', name='password_reset_confirm'),
    # path('accounts/reset/done/', name='password_reset_complete'),
    # path('contact/', views.contact),
    # path('contact/', views.contact),
]
