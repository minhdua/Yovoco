from cryptography.fernet import Fernet
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from yovoco.constants import *

def send_email(subject, message, to_email):
	email=EmailMessage(subject, message, to=[to_email])
	email.send()

def get_random_otp_code():
	return get_random_string(length=6, allowed_chars=VALUE_ALLOWED_NUMBER_CHAR)

# JWT Utils
def encrypt_message(message):
	key=settings.SCRYPT_SECRET_KEY
	fernet=Fernet(key)
	return fernet.encrypt(message.encode()).decode()
	
def decrypt_message(message):
	key=settings.SCRYPT_SECRET_KEY
	fernet=Fernet(key)
	decode=fernet.decrypt(message.encode()).decode()
	return decode

def is_expired(expiry_time):
	"""
	Returns true if the time is expired.
	"""
	return datetime.now() > expiry_time