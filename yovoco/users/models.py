from django.db import models
from django.contrib.auth.models import AbstractUser
from picklefield.fields import PickledObjectField
from rest_framework import exceptions

class Verification:
	def __init__(self, is_verified=False, verification_key=None, verification_expiry=None, verification_at=None):
		self.is_verified=is_verified
		self.verification_key=verification_key
		self.verification_expiry=verification_expiry
		self.verification_at=verification_at
	

class CustomUser(AbstractUser):
	first_name=models.CharField(max_length=30, blank=True, null=True)
	last_name=models.CharField(max_length=30, blank=True, null=True)
	mobile_number=models.CharField(max_length=10, blank=True, null=True)
	address=models.CharField(max_length=255, blank=True, null=True)
	verified_email=PickledObjectField(default=dict)
	verified_mobile_number=PickledObjectField(default=dict)
	reset_password=PickledObjectField(default=dict)
	avartar=models.URLField(blank=True, null=True,default='avartar/default.png')
	last_updated=models.DateTimeField(auto_now=True)
	email=models.EmailField(blank=True, null=True)
	city=models.CharField(max_length=255, blank=True, null=True)
	country=models.CharField(max_length=255, blank=True, null=True)
	postal_code=models.CharField(max_length=255, blank=True, null=True)
	birthday=models.DateField(blank=True, null=True)

	@classmethod
	def get_by_email(cls,email):
		users=CustomUser.objects.filter(email=email).all()
		for user in users:
			if user.verified_email.get('is_verified',False):
				return user
		raise exceptions.NotFound('User not found')

	class Meta:
		db_table='auth_user'
