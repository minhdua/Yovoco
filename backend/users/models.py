from django.contrib.auth.models import AbstractUser
from django.db import models
from picklefield.fields import PickledObjectField
from rest_framework import exceptions
from yovoco.constants import VALUE_AUTH_USER, VALUE_DEFAULT_AVATAR 
class Verification:
	def __init__(self, is_verified=False, verification_key=None, verification_expiry=None, verification_at=None):
		self.is_verified=is_verified
		self.verification_key=verification_key
		self.verification_expiry=verification_expiry
		self.verification_at=verification_at
	

class CustomUser(AbstractUser):
	username=models.CharField(max_length=255,unique=True, blank=True, null=True)
	password=models.CharField(max_length=255, blank=True, null=True)
	first_name=models.CharField(max_length=30, blank=True, null=True)
	last_name=models.CharField(max_length=30, blank=True, null=True)
	mobile_number=models.CharField(max_length=10, blank=True, null=True)
	address=models.CharField(max_length=255, blank=True, null=True)
	verified_email=PickledObjectField(default=dict)
	verified_mobile_number=PickledObjectField(default=dict)
	reset_password=PickledObjectField(default=dict)
	avartar=models.URLField(blank=True, null=True,default=VALUE_DEFAULT_AVATAR)
	last_updated=models.DateTimeField(auto_now=True)
	email=models.EmailField(blank=True, null=True)
	city=models.CharField(max_length=255, blank=True, null=True)
	country=models.CharField(max_length=255, blank=True, null=True)
	postal_code=models.CharField(max_length=255, blank=True, null=True)
	birthday=models.DateField(blank=True, null=True)
	class Meta:
		db_table=VALUE_AUTH_USER
