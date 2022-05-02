from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt import exceptions
from users.models import CustomUser, Verification
from users.utils import get_random_otp_code
from datetime import datetime, timedelta

class VerifyEmailToken(RefreshToken):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def for_user(cls, user):
		"""
		Adds this token to the outstanding token list.
		"""
		token=super().for_user(user)
		otp_code=get_random_otp_code()
		token['verification_key']=otp_code
		token['email']=user.email
		token['type']='verify_email'
		user_id=token.get('user_id')
		user=CustomUser.objects.get(id=user_id)

		verified_email=Verification(
			is_verified=False,
			verification_key=otp_code,
			verification_expiry=datetime.now() + timedelta(minutes=5),
			verification_at=datetime.now()
		)
		user.verified_email=verified_email.__dict__
		user.save()
		return token

class ResetPasswordToken(RefreshToken):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def for_user(cls, user):
		"""
		Adds this token to the outstanding token list.
		"""
		token=super().for_user(user)
		otp_code=get_random_otp_code()
		token['verification_key']=otp_code
		token['type']='reset_password'
		user_id=token.get('user_id')
		user=CustomUser.objects.get(id=user_id)
		user.password_reset.verification_key=otp_code
		user.password_reset.verification_expiry=datetime.timedelta(minutes=5)
		user.password_reset.verification_at=datetime.now()
		user.password_reset.save()
		return token

def get_verifytoken_for_user(user):
	"""
	Returns a token for a given user.
	"""
	user=CustomUser.objects.get(id=user.id)
	refresh=VerifyEmailToken.for_user(user=user)

	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}

def get_token_for_user(user):
	"""
	Returns a token for a given user.
	"""
	user=CustomUser.objects.get(id=user.id)
	refresh=RefreshToken.for_user(user=user)
	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}

def get_user_from_token(token):
	"""
	Returns a user from a token.
	"""
	try:
		refresh=RefreshToken(token)
		user=refresh.user
	except TokenError:
		raise exceptions.AuthenticationFailed('Invalid token')

	return user

def get_reset_password_token_for_user(user):
	"""
	Returns a token for a given user.
	"""
	user=CustomUser.objects.get(id=user.id)
	refresh=ResetPasswordToken.for_user(user=user)

	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}
