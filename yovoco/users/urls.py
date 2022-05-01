from users import views
from django.urls import path

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh, name='refresh'),
    path('logout/', views.logout, name='logout'),
    path('logout-everywhere/', views.logout_everywhere, name='logout-everywhere'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('verify-email/', views.verify_mail, name='verify-email'),
    path('reverify-email/', views.reverify_verification_mail, name='reverify-email'),
]
