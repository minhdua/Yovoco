from collections import OrderedDict
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers, status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
import re
from users import models, response, tokens , utils
from yovoco.constants import *


def get_body_verification_mail(username, hostname, key):
	return f'''
	Dear {username},

	Welcome to Yovoco!
	
	Thank you for registering with us.
	Please click on the link below to verify your email address.

	http://{hostname}/api/v1/user/verify_email/?key={key}

	Regards,
	Team Yovoco
	'''

def get_subject_verification_mail():
	return VALUE_SUBJECT_VERIFICATION_EMAIL

class NonNullModelSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		result=super(NonNullModelSerializer, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key]])

class ProfileSerializer(NonNullModelSerializer):
	'''
	Profile serializer
	Display user profile
	'''
	class Meta:
		model=models.CustomUser
		fields=(KEY_USERNAME, KEY_EMAIL, KEY_AVARTAR, KEY_MOBILE_NUMBER,\
		KEY_FIRST_NAME, KEY_LAST_NAME, KEY_ADDRESS, KEY_CITY, KEY_COUNTRY,\
		KEY_POSTAL_CODE, KEY_BIRTHDAY)
		extra_kwargs={
			KEY_BIRTHDAY: {KEY_FORMAT: VALUE_STRING_FORMAT_DATE},
		}
	def get(self):
		return response.ResultResponse(MESSAGE_GET_PROFILE_SUCCESS, data=self.data).get_response

def validate_password(value):
	'''
	Validate password
		required: true
		min_length: 8
		max_length: 20
		regex: digits, upper, lower, not special
	'''
	if value is None:
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_REQUIRED)
	if len(value) < VALUE_VALIDATION_PASSWORD_MIN_LENGTH:
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_LEAST_CHARACTER)
	if len(value) > VALUE_VALIDATION_PASSWORD_MAX_LENGTH:
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_MOST_CHARACTER)
	if not any(char.isdigit() for char in value):
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_CONTAIN_DIGIT)
	if not any(char.isupper() for char in value):
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_CONTAIN_UPPERCASE)
	if not any(char.islower() for char in value):
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_CONTAIN_LOWERCASE)
	if any(not char.isalnum() for char in value):
		raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_NOT_CONTAIN_SPECIAL_CHARACTER)
	return value

def check_email_exists(email):
	"""
	Check if email exists in database
	exclude email verified
	"""
	users=models.CustomUser.objects.filter(email=email)
	for user in users:
		if user.verified_email.get(KEY_IS_VERIFIED,False):
			return True
	return False

def check_mobile_number_exists(mobile_number):
	"""
	Check if mobile number exists in database
	exclude mobile number verified
	"""
	users=models.CustomUser.objects.filter(mobile_number=mobile_number)
	for user in users:
		if user.verified_mobile_number.get(KEY_IS_VERIFIED,False):
			return True
	return False
class RegistrationSerializer(NonNullModelSerializer):
	'''
	Registration serializer
	Register user and send verification email.
	'''

	password2=serializers.CharField(style={KEY_INPUT_TYPE: VALUE_PASSWORD}, write_only=True, allow_null=True)
	class Meta:
		model=models.CustomUser
		fields=[KEY_USERNAME, KEY_EMAIL, KEY_MOBILE_NUMBER, KEY_PASSWORD, KEY_PASSWORD2]
  

	def validate_username(self, value):
		'''
		validate username.
			required: true
			min_length: 5
			max_length: 20
			regex: contains at least one lowercase letter, one uppercase letter, and one digit
			unique: true
		'''
		if value is None:
			raise serializers.ValidationError(MESSAGE_VALIDATION_USERNAME_REQUIRED)
		if len(value) < VALUE_VALIDATION_USERNAME_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_USERNAME_LEAST_CHARACTER)
		if len(value) > VALUE_VALIDATION_USERNAME_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_USERNAME_MOST_CHARACTER)
		if not any (char.isdigit() for char in value) or not any (char.isalpha() for char in value):
			raise serializers.ValidationError(MESSAGE_VALIDATION_USERNAME_CONTAIN_LETTER_AND_DIGIT)
		if not value.isalnum():
			raise serializers.ValidationError(MESSAGE_VALIDATION_USERNAME_NOT_CONTAIN_SPECIAL_CHARACTER)
		if models.CustomUser.objects.filter(username=value).exists():
			raise serializers.ValidationError(MESSAGE_USERNAME_EXIST)
		return value

	def validate_email(self, value):
		'''
		validate email.
			required: true
			unique: true
			min_length: 5
			max_length: 50
			regex: email
		'''
		if value is None:
			raise serializers.ValidationError(MESSAGE_VALIDATION_EMAIL_REQUIRED)
		if len(value) < VALUE_VALIDATION_EMAIL_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_EMAIL_LEAST_CHARACTER)
		if len(value) > VALUE_VALIDATION_EMAIL_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_EMAIL_MOST_CHARACTER)
		if not re.fullmatch(VALUE_VALIDATION_REGEX_EMAIL, value):
			raise serializers.ValidationError(MESSAGE_EMAIL_INVALID)
		if check_email_exists(value):
			raise serializers.ValidationError(MESSAGE_EMAIL_EXIST)
		return value

	def validate_mobile_number(self, value):
		'''
		validate mobile number.
			required: true
			unique: true
			min_length: 10
			max_length: 10
			regex: digits
		'''
		if value is None:
			raise serializers.ValidationError(MESSAGE_VALIDATION_MOBILE_NUMBER_REQUIRED)
		if len(value) < VALUE_VALIDATION_MOBILE_NUMBER_LENGTH and len(value) > VALUE_VALIDATION_MOBILE_NUMBER_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_MOBILE_NUMBER_LENGTH)
		if not re.fullmatch(VALUE_VALIDATION_MOBILE_NUMBER_REGEX, value):
			raise serializers.ValidationError(MESSAGE_MOBILE_NUMBER_INVALID)
		if check_mobile_number_exists(value):
			raise serializers.ValidationError(MESSAGE_MOBILE_NUMBER_EXIST)
		return value

	def validate_password(self, value):
		'''
		validate password.
		'''
		return validate_password(value)

	def validate_password2(self, value):
		'''
		validate password.
		'''
		if value is None:
			raise serializers.ValidationError(MESSAGE_VALIDATION_REPEAT_PASSWORD_REQUIRED)
		return value

	@transaction.atomic
	def save(self):
		'''
		save user. if password is valid and match, then save user, 
 		else return error. Then send verification email.
		'''
		email=self.validated_data.get(KEY_EMAIL)
		username=self.validated_data.get(KEY_USERNAME)
		user=models.CustomUser(email=email, username=username)
		password=self.validated_data.get(KEY_PASSWORD)
		password2=self.validated_data.get(KEY_PASSWORD2)
		
  
		if password != password2:
			raise serializers.ValidationError({"password2":[MESSAGE_VALIDATION_PASSWORD_NOT_MATCH]})
		user.set_password(password)
		user.save()
		return self.send_verification_email(user)

	def send_verification_email(self, user):
		'''
		send verification email.
		'''
		subject=get_subject_verification_mail()
		current_site=settings.SERVER_HOST
		token=tokens.get_verify_token_for_user(user).get(KEY_ACCESS)
		key_encrypted=utils.encrypt_message(token)
		mail_body=get_body_verification_mail(user.username, current_site, key_encrypted)
		utils.send_email(subject, mail_body, user.email)
		data=response.ResultResponse(MESSAGE_REGISTER_SUCCESS,
		status_code=status.HTTP_201_CREATED, data=self.data)
		return data.get_response

class VerifiedMailSerializer(serializers.Serializer):
	'''
	Verified mail serializer.
	'''
	key=serializers.CharField()

	def validate_key(self, value):
		'''
		validate key. raise error if key is invalid.
		'''

		key_decrypted=utils.decrypt_message(value)
		if not key_decrypted:
			raise serializers.ValidationError(MESSAGE_INVALID_KEY)
		return key_decrypted

	def save(self):
		'''
		verify user email. raise error if verification fails.
		'''
		key=self.validated_data.get(KEY_KEY)
		try:
			payload=AccessToken(key).payload
			user_id=payload.get(KEY_USER_ID)
			verification_key=payload.get(KEY_VERIFICATION_KEY)
			email=payload.get(KEY_EMAIL)
			token_type=payload.get(KEY_TYPE)
		except TokenError as e:
			raise serializers.ValidationError({KEY_DETAIL:e})
		if token_type != VALUE_VERIFY_EMAIL:
			raise serializers.ValidationError(MESSAGE_TOKEN_TYPE_INVALID)
		user=models.CustomUser.objects.get(id=user_id)
		if user.verified_email.get(KEY_IS_VERIFIED):
			raise serializers.ValidationError(MESSAGE_EMAIL_ALREADY_VERIFIED)
		if user.verified_email.get(KEY_VERIFICATION_KEY) != verification_key:
			raise serializers.ValidationError(MESSAGE_ACCESS_DENIED)
		if user.verified_email.get(KEY_VERIFICATION_EXPIRY) < datetime.now():
			raise serializers.ValidationError(MESSAGE_LINK_EXPIRED)
		user.verified_email[KEY_IS_VERIFIED]=True
		user.email=email
		user.save()
		return response.ResultResponse(detail=MESSAGE_VERIFIED_SUCCESS,data={
																		KEY_USERNAME: user.username,
																		KEY_EMAIL: user.email,
																	}).get_response

class ReverifyMailSerializer(serializers.Serializer):
	'''
	re-verify mail serializer.
	'''
	username=serializers.CharField()
	email=serializers.EmailField()
	
	def validate_username(self, value):
		'''
		validate username. raise error if username is invalid.
		'''
		if not models.CustomUser.objects.filter(username=value).exists():
			raise serializers.ValidationError(MESSAGE_USERNAME_NOT_EXISTS)
		return value

	def save(self):
		'''
		resent verification email.
		'''
		return self.resend_verification_email()

	def resend_verification_email(self):
		'''
		resend verification email.
		'''
		username=self.validated_data.get(KEY_USERNAME)
		user=models.CustomUser.objects.filter(username=username).first()
		email=self.validated_data.get(KEY_EMAIL)
		if email != user.email:
			user.email=email
			user.save()
		subject=get_subject_verification_mail()
		current_site=settings.SERVER_HOST
		token=tokens.get_verify_token_for_user(user).get(KEY_ACCESS)
		key_encrypted=utils.encrypt_message(token)
		mail_body=get_body_verification_mail(user.username, current_site, key_encrypted)
		utils.send_email(subject, mail_body, user.email)
		return response.ResultResponse(detail=MESSAGE_EMAIL_RESENT_SUCCESS, data={
																				KEY_USERNAME: user.username,
																				KEY_EMAIL: user.email,
																			}).get_response

class LoginSerializer(serializers.Serializer):
	'''
	Login serializer.
	'''
	username=serializers.CharField()
	password=serializers.CharField(style={KEY_INPUT_TYPE: VALUE_PASSWORD}, write_only=True)

	def validate(self, data):
		'''
		validate username and password.
		'''
		if data:
			username=data.get(KEY_USERNAME)
			password=data.get(KEY_PASSWORD)
			if username and password :
				user=authenticate(username=username, password=password)
				if user:
					if user.is_active:
						token=tokens.get_token_for_user(user)
					else:
						msg=MESSAGE_USER_NOT_ACTIVE
						raise serializers.ValidationError(msg)
				else:
					msg=MESSAGE_UNABLE_TO_LOGIN_WITH_PROVIDER
					raise serializers.ValidationError(msg)
			else:
				msg=MESSAGE_MUST_INCLUDE_USERNAME
				raise serializers.ValidationError(msg)
		return response.ResultResponse(detail=MESSAGE_LOGIN_SUCCESS, data=token).get_response
class ProfileUpdateSerializer(NonNullModelSerializer):
	class Meta:
		model=models.CustomUser
		fields=(KEY_USERNAME, KEY_EMAIL, KEY_AVARTAR, KEY_MOBILE_NUMBER, KEY_FIRST_NAME, \
   				KEY_LAST_NAME, KEY_ADDRESS, KEY_CITY, KEY_COUNTRY, KEY_POSTAL_CODE, KEY_BIRTHDAY)
		extra_kwargs={
			KEY_USERNAME: {KEY_READ_ONLY: True},
		}

	def validate_mobile_number(self, value):
		if not re.fullmatch(VALUE_VALIDATION_MOBILENUMBER_REGEX, value):
			raise serializers.ValidationError(MESSAGE_MOBILENUMBER_INVALID)
		if value and models.CustomUser.objects.filter(mobile_number=value).exclude(id=self.instance.id).exists():
			raise serializers.ValidationError(MESSAGE_MOBILE_NUMBER_EXIST)
		return value

	def validate_email(self, value):
		if value and models.CustomUser.objects.filter(email=value).exclude(id=self.instance.id).exists():
			if check_email_exists(value):
				raise serializers.ValidationError(MESSAGE_EMAIL_EXIST)
		return value

	def validate_avatar(self, value):
		if value and value.size > VALUE_IMAGE_MAX_SIZE:
			raise serializers.ValidationError(MESSAGE_IMAGE_SIZE_TOO_LARGE)
		if value and value.content_type not in VALUE_IMAGE_CONTENT_TYPES:
			raise serializers.ValidationError(MESSAGE_IMAGE_TYPE_INVALID)
		return value

	def update(self, instance, validated_data):
		self.instance.email=validated_data.get(KEY_EMAIL, instance.email)
		self.instance.avartar=validated_data.get(KEY_AVARTAR, instance.avartar)
		self.instance.mobile_number=validated_data.get(KEY_MOBILE_NUMBER, instance.mobile_number)
		self.instance.first_name=validated_data.get(KEY_FIRST_NAME, instance.first_name)
		self.instance.last_name=validated_data.get(KEY_LAST_NAME, instance.last_name)
		self.instance.address=validated_data.get(KEY_ADDRESS, instance.address)
		self.instance.city=validated_data.get(KEY_CITY, instance.city)
		self.instance.country=validated_data.get(KEY_COUNTRY, instance.country)
		self.instance.postal_code=validated_data.get(KEY_POSTAL_CODE, instance.postal_code)
		self.instance.birthday=validated_data.get(KEY_BIRTHDAY, instance.birthday)
		self.instance.last_updated=datetime.now()
		self.instance.save()
		return response.ResultResponse(detail=MEASSAGE_PROFILE_UPDATE_SUCCESS,
						data=ProfileUpdateSerializer(self.instance).data).get_response

class PasswordUpdateSerializer(serializers.Serializer):
	old_password=serializers.CharField(required=True)
	new_password=serializers.CharField(required=True)
	new_password2=serializers.CharField(required=True)

	class Meta:
		fields=(KEY_OLD_PASSWORD, KEY_NEW_PASSWORD, KEY_NEW_PASSWORD2)
		extra__kwargs={
			KEY_OLD_PASSWORD: {KEY_WRITE_ONLY: True},
			KEY_NEW_PASSWORD: {KEY_WRITE_ONLY: True},
			KEY_NEW_PASSWORD2: {KEY_WRITE_ONLY: True},
		}

	def validate_old_password(self, value):
		if not self.instance.check_password(value):
			raise serializers.ValidationError(MESSAGE_PASSWORD_INCORRECT)
		return value

	def validate(self, data):
		if validate_password(data.get(KEY_NEW_PASSWORD)) != data.get(KEY_NEW_PASSWORD2):
			raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_NOT_MATCH)
		return data

	def update(self, instance, validated_data):
		new_password=validated_data.get(KEY_NEW_PASSWORD)
		instance.set_password(new_password)
		instance.save()
		return response.ResultResponse(detail=MESSAGE_PASSWORD_UPDATE_SUCCESS).get_response

def get_subject_reset_password_mail():
	return VALUE_RESET_PASSWORD

def get_body_reset_password_mail(username, current_site, key_encrypted):
	return f'''
		Dear {username},

		You have requested to reset your password.

		Please click on the following link to reset your password:
		{current_site}/api/v1/user/reset_password/?key={key_encrypted}

		If you did not make this request, please ignore this email.
		This is an automated email. Please do not reply to this email.

		Thank you,
		{settings.SERVER_NAME} Team.
	'''

class PasswordResetSerializer(serializers.Serializer):
	email=serializers.EmailField()

	def validate_email(self, value):
		if not models.CustomUser.objects.filter(email=value).exists():
			raise serializers.ValidationError(MESSAGE_EMAIL_NOT_EXIST)
		return value

	def save(self):
		return self.reset_password()

	def reset_password(self):
		email=self.validated_data.get(KEY_EMAIL)
		user=models.CustomUser.objects.get(email=email)
		subject=get_subject_reset_password_mail()
		current_site=settings.SERVER_HOST
		token=tokens.get_reset_password_token_for_user(user).get(KEY_ACCESS)
		key_encrypted=tokens.encrypt_message(token)
		mail_body=get_body_reset_password_mail(user.username, current_site, key_encrypted)
		utils.send_email(subject, mail_body, user.email)
		data=response.ResultResponse(detail=MESSAGE_RESET_PASSWORD_SUCCESS, data=self.data)
		return data.get_response

class VerifyResetPasswordSerializer(serializers.Serializer):
	key=serializers.CharField()

	def validate_key(self, value):
		if not utils.decrypt_message(value):
			raise serializers.ValidationError({KEY_DETAIL:VALUE_INVALID_KEY})
		return value

	def save(self):
		return self.verify_reset_password()

	def verify_reset_password(self):
		key=self.validated_data.get(KEY_KEY)
		token=utils.decrypt_message(key)
		try:
			payload=AccessToken(token).payload
			user_id=payload.get(KEY_USER_ID)
			verification_key=payload(KEY_VERIFICATION_KEY)
			token_type=payload(KEY_TYPE)
		except TokenError as e:
			raise serializers.ValidationError(e)
		if token_type != VALUE_RESET_PASSWORD:
			raise serializers.ValidationError(VALUE_INVALID_KEY)
		user=models.CustomUser.objects.get(id=user_id)
		if not user.email.is_verified:
			raise serializers.ValidationError(MESSAGE_VERIFY_EMAIL_FIRST)
		if user.reset_password.verification_key != verification_key:
			raise serializers.ValidationError({KEY_DETAIL:VALUE_INVALID_KEY})
		if user.reset_password.verification_at + user.reset_password.verification_expiry < datetime.now():
			raise serializers.ValidationError(MESSAGE_KEY_HAS_EXPIRED)
		user.save()
		return response.ResultResponse(detail=MESSAGE_SEND_RESET_PASSWORD_SUCCESS, data=tokens.get_token_for_user(user)).get_response

class PasswordResetConfirmSerializer(serializers.Serializer):
	access_token=serializers.CharField(required=True)
	KEY_NEW_PASSWORD=serializers.CharField(required=True)
	KEY_NEW_PASSWORD2=serializers.CharField(required=True)

	def validate(self, data):
		if validate_password(data.get(KEY_NEW_PASSWORD)) != data.get(KEY_NEW_PASSWORD2):
			raise serializers.ValidationError(MESSAGE_VALIDATION_PASSWORD_NOT_MATCH)
		return data

	def save(self):
		return self.reset_password()

	def reset_password(self):
		token=self.validated_data.get(VALUE_ACCESS_TOKEN)
		try:
			payload=AccessToken(token).payload
			user_id=payload.get(KEY_USER_ID)
		except TokenError as e:
			raise serializers.ValidationError({KEY_DETAIL:e})
		user=models.CustomUser.objects.get(id=user_id)
		KEY_NEW_PASSWORD=self.validated_data.get(KEY_NEW_PASSWORD)
		user.set_password(KEY_NEW_PASSWORD)
		user.save()
		return response.ResultResponse(detail=MESSAGE_RESET_PASSWORD_SUCCESS, data=self.data).get_response

class LogoutSerializer(serializers.Serializer):
	refresh_token=serializers.CharField(required=True)
	
	def validate(self, data):
		self.token=data.get(KEY_REFRESH_TOKEN)
		return data

	def logout(self):
		try:
			RefreshToken(self.token).blacklist()
			return response.ResultResponse(detail=MESSAGE_LOGOUT_SUCCESS,
		status_code=status.HTTP_205_RESET_CONTENT).get_response
		except TokenError as e:
			raise serializers.ValidationError({KEY_DETAIL:e})
		
class LogoutEverywhereSerializer(serializers.Serializer):
	def logout_everywhere(self,user):
		for token in OutstandingToken.objects.filter(user=user):
			_, _=BlacklistedToken.objects.get_or_create(token_id=token.id)
		return response.ResultResponse(detail=MESSAGE_LOGOUT_EVERYWHERE_SUCCESS,
		status_code=status.HTTP_205_RESET_CONTENT).get_response
		
class RefreshTokenSerializer(serializers.Serializer):
	refresh_token=serializers.CharField(required=True)

	def validate(self, data):
		self.token=data.get(KEY_REFRESH_TOKEN)
		return data

	def refresh(self):
		try:
			refresh=RefreshToken(self.token)
			if settings.SIMPLE_JWT.get(KEY_ROTATE_REFRESH_TOKENS) and\
						settings.SIMPLE_JWT.get(KEY_BLACKLIST_AFTER_ROTATION):
				refresh.blacklist()
			refresh.set_jti()
			refresh.set_exp()
			refresh.set_iat()
			return response.ResultResponse(detail=MESSAGE_REFRESH_TOKEN_SUCCESS, data={
			KEY_REFRESH: str(refresh),
			KEY_ACCESS: str(refresh.access_token)}).get_response
		except TokenError as e:
			raise serializers.ValidationError({KEY_DETAIL:e})