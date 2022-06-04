from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.serializers import (ProfileSerializer, 
									RegistrationSerializer, 
									LoginSerializer, 
									ProfileUpdateSerializer, 
									PasswordUpdateSerializer,
									VerifiedMailSerializer,
									ReverifyMailSerializer,
									PasswordResetSerializer,
									VerifyResetPasswordSerializer,
									PasswordResetConfirmSerializer,
									LogoutEverywhereSerializer,
									LogoutSerializer,
									RefreshTokenSerializer,)
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from yovoco.constants import *

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def registration(request):
	"""
	Registration view
	"""
	serializer=RegistrationSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_GET_METHOD])
@permission_classes([AllowAny])
def verify_mail(request):
	"""
	Verify email address view
	"""
	key_encrypted=request.GET.get(KEY_KEY)
	serializer=VerifiedMailSerializer(data={KEY_KEY: key_encrypted})
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def reverify_verification_mail(request):
	serializer=ReverifyMailSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def login(request):
	serializer=LoginSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.validated_data
		return Response(response, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_GET_METHOD])
def profile(request):
	"""
	Profile view
	"""
	if request.method == VALUE_GET_METHOD:
		user=request.user
		response=ProfileSerializer(user).get()
		return Response(response, status=status.HTTP_200_OK)
	raise exceptions.MethodNotAllowed(request.method)

@api_view([VALUE_PUT_METHOD])
def update_profile(request):
	user=request.user
	serializer=ProfileUpdateSerializer(user, data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_PUT_METHOD])
def change_password(request):
	user=request.user
	serializer=PasswordUpdateSerializer(user, data=request.data, context={KEY_REQUEST: request})
	if serializer.is_valid():
		response=serializer.update(request.user, serializer.validated_data)
		return Response(response, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def reset_password(request):
	serializer=PasswordResetSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_GET_METHOD])
@permission_classes([AllowAny])
def verify_reset_password(request):
	serializer=VerifyResetPasswordSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def reset_password_confirm(request):
	serializer=PasswordResetConfirmSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.save()
		return Response(response, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_DELETE_METHOD])
@permission_classes([AllowAny])
def logout(request):
	serializer=LogoutSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.logout()
		return Response(response, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([VALUE_DELETE_METHOD])
def logout_everywhere(request):
	serializer=LogoutEverywhereSerializer(data=request.data)
	response=serializer.logout_everywhere(request.user)
	return Response(response, status=status.HTTP_200_OK)

@api_view([VALUE_POST_METHOD])
@permission_classes([AllowAny])
def refresh(request):
	serializer=RefreshTokenSerializer(data=request.data)
	if serializer.is_valid():
		response=serializer.refresh()
		return Response(response, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	