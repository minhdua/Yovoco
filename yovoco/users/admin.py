from django.contrib import admin
from users.models import CustomUser
from django.db import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display=('username', 'email', 'first_name', 'last_name', 'is_staff')
	search_fields=('username', 'email', 'first_name', 'last_name')
	list_filter=('is_staff', 'is_superuser', 'is_active', 'groups')
	fieldsets=(
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
	)

	formfield_overrides={
		models.TextField: {'widget': admin.widgets.AdminTextInputWidget},
	}

	add_fieldsets=(
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2')}
		),
	)
	ordering=('username',)

admin.site.register(CustomUser, UserAdmin)