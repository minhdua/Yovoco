from django.conf import settings
from django.db import transaction
from rest_framework import serializers, exceptions
from users.models import CustomUser, Verification
from django.contrib.auth import authenticate
from users.tokens import (get_verifytoken_for_user, 
                            get_token_for_user, 
                            get_reset_password_token_for_user,)
from users.utils import encrypt_message,decrypt_message ,send_email
from users.response import ResultResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from collections import OrderedDict
from datetime import datetime
from rest_framework import status
from uuid import uuid4

INVALID_KEY = 'Invalid key'

def validate_password(value):
    if len(value) < 8:
        raise serializers.ValidationError({'detail':'Password must be at least 8 characters long'})
    if len(value) > 20:
        raise serializers.ValidationError({'detail':'Password must be at most 20 characters long'})
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError({'detail':'Password must contain at least one digit'})
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError({'detail':'Password must contain at least one uppercase letter'})
    return value

def check_email_exists(email):
    users = CustomUser.objects.filter(email=email)
    for user in users:
       if user.verified_email['is_verified']:
           return True
    return False

def get_body_verification_mail(username, hostname, key):
    return f'''
    Dear {username},

    Welcome to Yovoco!
    
    Thank you for registering with us.
    Please click on the link below to verify your email address.

    http://{hostname}/api/v1/verify-email?key={key}

    Regards,
    Team Yovoco
    '''

def get_subject_verification_mail():
    return 'Verify your email address to complete registration'

class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(NonNullModelSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class ProfileSerializer(NonNullModelSerializer):
    '''
    Profile serializer
    Display user profile
    '''
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avartar', 'mobile_number','first_name', 'last_name', 'address', 'city', 'country', 'postal_code', 'birthday')
        extra_kwargs = {
            'birthday': {'format': '%d-%m-%Y'},
        }
    def get(self):
        return ResultResponse(detail ='Get profile successfully', status_code = status.HTTP_200_OK, data = self.data).get_response

class RegistrationSerializer(NonNullModelSerializer):
    '''
    Registration serializer
    Register user and send verification email.
    '''

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'token', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        '''
        validate username. 
        '''
        if len(value) < 5:
            raise serializers.ValidationError({'detail':'Username must be at least 5 characters long.'})
        if len(value) > 20:
            raise serializers.ValidationError({'detail':'Username cannot be more than 20 characters long.'})
        if not value.isalnum():
            raise serializers.ValidationError({'detail':'Username can only contain letters and numbers.'})
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({'detail':'Username already exists.'})
        return value

    def validate_email(self, value):
        '''
        validate email.
        '''
        if len(value) < 5:
            raise serializers.ValidationError({'detail':'Email must be at least 5 characters long.'})
        if len(value) > 100:
            raise serializers.ValidationError({'detail':'Email cannot be more than 100 characters long.'})
        if check_email_exists(value):
            raise serializers.ValidationError({'detail':'Email already exists.'})
        return value

    def validate_mobile_number(self, value):
        '''
        validate mobile number.
        '''
        if len(value) < 10:
            raise serializers.ValidationError({'detail':'Mobile number must be at least 10 characters long.'})
        if len(value) > 10:
            raise serializers.ValidationError({'detail':'Mobile number cannot be more than 10 characters long.'})
        if not value.isalpha():
            raise serializers.ValidationError({'detail':'Mobile number can only contain letters.'})
        if CustomUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError({'detail':'Mobile number already exists.'})
        return value

    def validate_password(self, value):
        '''
        validate password.
        '''
        return validate_password(value)

    @transaction.atomic
    def save(self):
        '''
        save user. if password is valid and match, then save user, else return error. Then send verification email.
        '''
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if self.validate_password(password) != password2:
            raise serializers.ValidationError({'detail':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return self.send_verification_email(user)

    def send_verification_email(self, user):
        '''
        send verification email.
        '''
        subject = get_subject_verification_mail()
        current_site = settings.SERVER_HOST
        token = get_verifytoken_for_user(user).get('access')
        key_encrypted = encrypt_message(token)
        mail_body = get_body_verification_mail(user.username, current_site, key_encrypted)
        send_email(subject, mail_body, user.email)
        data = ResultResponse(detail='Register Successfully. Please verify your email address.',
        status_code=status.HTTP_201_CREATED, data=self.data)
        return data.get_response

class VerifiedMailSerializer(serializers.Serializer):
    '''
    Verified mail serializer.
    '''
    key = serializers.CharField()

    def validate_key(self, value):
        '''
        validate key. raise error if key is invalid.
        '''

        key_decrypted = decrypt_message(value)
        if not key_decrypted:
            raise serializers.ValidationError({'detail':INVALID_KEY})
        return key_decrypted

    def save(self):
        '''
        verify user email. raise error if verification fails.
        '''
        key = self.validated_data['key']
        try:
            payload = AccessToken(key).payload
            user_id = payload['user_id']
            verification_key = payload['verification_key']
            email = payload['email']
            token_type = payload['type']
        except TokenError as e:
            raise serializers.ValidationError({'detail':e})
        if token_type != 'verify_email':
            raise serializers.ValidationError({'detail':'Invalid token type.'})
        user = CustomUser.objects.get(id=user_id)
        if user.verified_email.get('is_verified'):
            raise serializers.ValidationError({'detail':'Email already verified.'})
        if user.verified_email.get('verification_key') != verification_key:
            raise serializers.ValidationError({'detail':'This access has been revoked.'})
        if user.verified_email.get('verification_expiry') < datetime.now():
            raise serializers.ValidationError({'detail':'This link has expired.'})
        user.verified_email['is_verified'] = True
        user.email = email
        user.save()
        return ResultResponse(detail='Email verified successfully.',
        status_code=status.HTTP_200_OK, data={
            'username': user.username,
            'email': user.email,
        }).get_response

class ReverifyMailSerializer(serializers.Serializer):
    '''
    re-verify mail serializer.
    '''
    username = serializers.CharField()
    email = serializers.EmailField()
    
    def validate_username(self, value):
        '''
        validate username. raise error if username is invalid.
        '''
        if not CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({'detail':'Username does not exist.'})
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
        user = CustomUser.objects.filter(username=self.validated_data['username']).first()
        email = self.validated_data['email']
        if user.email != email:
            raise serializers.ValidationError({'detail':'This email is not associated with this username.'})
        if user.verified_email.get('is_verified'):
            raise serializers.ValidationError({'detail':'Email already verified.'})
        if user.verified_email.get('verification_expiry') > datetime.now():
            raise serializers.ValidationError({'detail':'Verify email sent to your email address. If you have not received the email, please check your spam folder. Wait for 5 minutes and try again.'})
        subject = get_subject_verification_mail()
        current_site = settings.SERVER_HOST
        token = get_verifytoken_for_user(user).get('access')
        key_encrypted = encrypt_message(token)
        mail_body = get_body_verification_mail(user.username, current_site, key_encrypted)
        send_email(subject, mail_body, user.email)
        data = ResultResponse(detail='Verification email sent successfully.',
        status_code=status.HTTP_200_OK, data=self.data)
        return data.get_response


class LoginSerializer(serializers.Serializer):
    '''
    Login serializer.
    '''
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        '''
        validate username and password.
        '''
        if data is not None:
            username = data.get('username', None)
            password = data.get('password', None)
            if username is not None and password is not None:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        token = get_token_for_user(user)
                    else:
                        msg = 'User is not active.'
                        raise serializers.ValidationError(msg)
                else:
                    msg = 'Unable to login with provided credentials.'
                    raise serializers.ValidationError(msg)
            else:
                msg = "Must include 'username' and 'password'."
                raise serializers.ValidationError(msg)
        return ResultResponse(detail='Login Successfully.',
        status_code=status.HTTP_200_OK, data=token).get_response


class ProfileUpdateSerializer(NonNullModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avartar', 'mobile_number', 'first_name', 'last_name', 'address', 'city', 'country', 'postal_code', 'birthday')
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def validate_mobile_number(self, value):
        if value is not None and len(value) != 10:
            raise serializers.ValidationError({'detail':'Mobile number must be 10 digits.'})
        if value is not None and not value.isdigit():
            raise serializers.ValidationError({'detail':'Mobile number must be numeric.'})
        if value is not None and CustomUser.objects.filter(mobile_number=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({'detail':'A user with that mobile number already exists.'})
        return value

    def validate_email(self, value):
        if value is not None and CustomUser.objects.filter(email=value).exclude(id=self.instance.id).exists():
            if check_email_exists(value):
                raise serializers.ValidationError({'detail':'A user with that email already exists.'})
        return value

    def validate_avatar(self, value):
        if value is not None and value.size > settings.MAX_IMAGE_SIZE:
            raise serializers.ValidationError({'detail':'Image size must be less than 2MB.'})
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.avartar = validated_data.get('avartar', instance.avartar)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.last_updated = datetime.now()
        instance.save()
        return ResultResponse(detail='You have successfully updated your profile.',
        status_code=status.HTTP_200_OK, data=ProfileUpdateSerializer(instance).data).get_response

class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        fields = ('old_password', 'new_password', 'new_password2')
        extra__kwargs = {
            'old_password' : {'write_only': True},
            'new_password' : {'write_only': True},
            'new_password2' : {'write_only': True},
        }


    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError({'detail':'Old password is incorrect.'})
        return value

    def validate(self, data):
        if validate_password(data['new_password']) != data['new_password2']:
            raise serializers.ValidationError({'detail':'Passwords do not match.'})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return ResultResponse(detail='Password updated successfully.',
        status_code=status.HTTP_200_OK).get_response

def get_subject_reset_password_mail():
    return 'Reset Password'

def get_body_reset_password_mail(username, current_site, key_encrypted):
    return f'''
        Dear {username},

        You have requested to reset your password.

        Please click on the following link to reset your password:
        {current_site}/auth/reset-password?key={key_encrypted}

        If you did not make this request, please ignore this email.
        This is an automated email. Please do not reply to this email.

        Thank you,
        {settings.SERVER_NAME} Team.
    '''

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({'detail':'Email does not exist.'})
        return value

    def save(self):
        return self.reset_password()

    def reset_password(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        subject = get_subject_reset_password_mail()
        current_site = settings.SERVER_HOST
        token = get_reset_password_token_for_user(user).get('access')
        key_encrypted = encrypt_message(token)
        mail_body = get_body_reset_password_mail(user.username, current_site, key_encrypted)
        send_email(subject, mail_body, user.email)
        data = ResultResponse(detail='Reset password link sent successfully.',
        status_code=status.HTTP_200_OK, data=self.data)
        return data.get_response

class VerifyResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField()

    def validate_key(self, value):
        if not decrypt_message(value):
            raise serializers.ValidationError({'detail':INVALID_KEY})
        return value

    def save(self):
        return self.verify_reset_password()

    def verify_reset_password(self):
        token = decrypt_message(self.validated_data['key'])
        try:
            payload = AccessToken(token).payload
            user_id = payload['user_id']
            verification_key = payload['verification_key']
            token_type = payload['type']
        except TokenError as e:
            raise serializers.ValidationError({'detail':e})
        if token_type != 'reset_password':
            raise serializers.ValidationError({'detail':INVALID_KEY})
        user = CustomUser.objects.get(id=user_id)
        if not user.email.is_verified:
            raise serializers.ValidationError({'detail':'Please verify your email first.'})
        if user.reset_password.verification_key != verification_key:
            raise serializers.ValidationError({'detail':INVALID_KEY})
        if user.reset_password.verification_at + user.reset_password.verification_expiry < datetime.now():
            raise serializers.ValidationError({'detail':'Key has expired.'})
        user.save()
        return ResultResponse(detail='Reset password link verified successfully.',
        status_code=status.HTTP_200_OK, data=get_token_for_user(user)).get_response

class PasswordResetConfirmSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if validate_password(data['new_password']) != data['new_password2']:
            raise serializers.ValidationError({'detail':'Passwords do not match.'})
        return data

    def save(self):
        return self.reset_password()

    def reset_password(self):
        token = self.validated_data['access_token']
        try:
            payload = AccessToken(token).payload
            user_id = payload['user_id']
        except TokenError as e:
            raise serializers.ValidationError({'detail':e})
        user = CustomUser.objects.get(id=user_id)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return ResultResponse(detail='Password reset successfully.',
        status_code=status.HTTP_200_OK, data=self.data).get_response

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    def validate(self, data):
      self.token = data['refresh_token']
      return data

    def logout(self):
        try:
            RefreshToken(self.token).blacklist()
            return ResultResponse(detail='Logout successfully.',
        status_code=status.HTTP_205_RESET_CONTENT).get_response
        except TokenError as e:
            raise serializers.ValidationError({'detail':e})
        
class LogoutEverywhereSerializer(serializers.Serializer):
    def logout_everywhere(self,user):
        for token in OutstandingToken.objects.filter(user=user):
            _, _ = BlacklistedToken.objects.get_or_create(token_id=token.id)
        return ResultResponse(detail='Loutout with all everywhere successful.',
        status_code=status.HTTP_205_RESET_CONTENT).get_response
        
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        self.token = data['refresh_token']
        return data

    def refresh(self):
        try:
            refresh = RefreshToken(self.token)
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS'] and settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                refresh.blacklist()
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            return ResultResponse(detail='Refresh token successfully.',
            status_code=status.HTTP_200_OK, data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),}).get_response
        except TokenError as e:
            raise serializers.ValidationError({'detail':e})
      
        
        