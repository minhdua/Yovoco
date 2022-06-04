from django.contrib import admin
from users.models import CustomUser
from django.db import models
from yovoco.constants import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display=(KEY_USERNAME, KEY_EMAIL, 'first_name', 'last_name', 'is_staff')
	search_fields=(KEY_USERNAME, KEY_EMAIL, 'first_name', 'last_name')
	list_filter=('is_staff', 'is_superuser', 'is_active', 'groups')
	fieldsets=(
		(None, {'fields': (KEY_USERNAME, 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', KEY_EMAIL)}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
	)

	formfield_overrides={
		models.TextField: {'widget': admin.widgets.AdminTextInputWidget},
	}

	add_fieldsets=(
		(None, {
			'classes': ('wide',),
			'fields': (KEY_USERNAME, 'password1', 'password2')}
		),
	)
	ordering=(KEY_USERNAME,)

admin.site.register(CustomUser, UserAdmin)
