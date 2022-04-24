from users import views
from django.urls import path

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('refresh', views.refresh, name='refresh'),
    path('logout', views.logout, name='logout'),
    path('logout-everywhere', views.logout_everywhere, name='logout_everywhere'),
    path('update-profile', views.update_profile, name='update_profile'),
    path('change-password', views.change_password, name='change_password'),
    path('verify-mail', views.verify_mail, name='verify_mail'),
    path('reverify-mail', views.reverify_verification_mail, name='reverify_mail'),
]
