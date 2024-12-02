# accounts/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserProfileSerializer
from django.db import transaction

# 마이페이지 조회 (GET 요청)
@api_view(['GET'])
def get_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

# 마이페이지 수정 (PUT 요청)
@api_view(['PUT'])
def update_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    profile_picture = request.FILES.get('profile_picture', None)
    bio = request.data.get('bio', user.bio)
    address = request.data.get('address', user.address)

    # 사용자 필드 업데이트
    user.username = request.data.get('username', user.username)
    user.email = request.data.get('email', user.email)
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.bio = bio
    user.address = address

    if profile_picture:
        user.profile_picture = profile_picture

    try:
        with transaction.atomic():
            user.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
