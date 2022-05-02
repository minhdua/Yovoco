from telnetlib import LOGOUT
from users import views
from django.urls import path

from yovoco.constants import *

urlpatterns=[
	path(PROFILE_URL, views.profile, name=VALUE_PROFILE),
	path(REGISTRATION_URL, views.registration, name=VALUE_REGISTRATION),
	path(LOGIN_URL, views.login, name=VALUE_LOGIN),
	path(REFRESH_URL, views.refresh, name=VALUE_REFRESH),
	path(LOGOUT_URL, views.logout, name=VALUE_LOGOUT),
	path(LOGOUT_EVERYWHERE_URL, views.logout_everywhere, name=VALUE_LOGOUT_EVERYWHERE),
	path(UPDATE_PROFILE_URL, views.update_profile, name=VALUE_UPDATE_PROFILE),
	path(CHANGE_PASSWORD_URL, views.change_password, name=VALUE_CHANGE_PASSWORD),
	path(VERIFY_EMAIL_URL, views.verify_mail, name=VALUE_VERIFY_EMAIL),
	path(REVERIFY_EMAIL_URL, views.reverify_verification_mail, name=VALUE_REVERIFY_EMAIL),
]
