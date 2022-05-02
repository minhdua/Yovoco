from datetime import datetime, timedelta
from rest_framework_simplejwt import exceptions, tokens
from users.models import CustomUser, Verification
from users.utils import get_random_otp_code
from yovoco.constants import *

class VerifyEmailToken(tokens.RefreshToken):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def for_user(cls, user):
		"""
		Adds this token to the outstanding token list.
		"""
		token=super().for_user(user)
		otp_code=get_random_otp_code()
		token[KEY_VERIFICATION_KEY]=otp_code
		token[KEY_EMAIL]=user.email
		token[KEY_TYPE]='verify_email'
		user_id=token.get(KEY_USER_ID)
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

class ResetPasswordToken(tokens.RefreshToken):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def for_user(cls, user):
		"""
		Adds this token to the outstanding token list.
		"""
		token=super().for_user(user)
		otp_code=get_random_otp_code()
		token[KEY_VERIFICATION_KEY]=otp_code
		token[KEY_TYPE]=VALUE_RESET_PASSWORD
		user_id=token.get(KEY_USER_ID)
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
		KEY_REFRESH: str(refresh),
		KEY_ACCESS: str(refresh.access_token),
	}

def get_token_for_user(user):
	"""
	Returns a token for a given user.
	"""
	user=CustomUser.objects.get(id=user.id)
	refresh=tokens.RefreshToken.for_user(user=user)
	return {
		KEY_REFRESH: str(refresh),
		KEY_ACCESS: str(refresh.access_token),
	}

def get_user_from_token(token):
	"""
	Returns a user from a token.
	"""
	try:
		refresh=tokens.RefreshToken(token)
		user=refresh.user
	except tokens.TokenError:
		raise exceptions.AuthenticationFailed(MESSAGE_INVALID_TOKEN)

	return user

def get_reset_password_token_for_user(user):
	"""
	Returns a token for a given user.
	"""
	user=CustomUser.objects.get(id=user.id)
	refresh=ResetPasswordToken.for_user(user=user)

	return {
		KEY_REFRESH: str(refresh),
		KEY_ACCESS: str(refresh.access_token),
	}
