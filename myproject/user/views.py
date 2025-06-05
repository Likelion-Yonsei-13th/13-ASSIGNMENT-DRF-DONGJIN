from django.shortcuts import render

# Create your views here.

from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def success(self, message, data=None, status_code=status.HTTP_200_OK):
        response_data = {"message": message}
        if data:
            response_data.update(data)
        return Response(response_data, status=status_code)
    
    def error(self, errors, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(errors, status=status_code)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success("회원가입이 완료되었습니다.", status_code=status.HTTP_201_CREATED)
        return self.error(serializer.errors)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerialzer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            response = self.success("로그인 성공")
            response["Authorization"] = f"Bearer {str(refresh.access_token)}"
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=False
            )
            return response
        return self.error(serializer.errors)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        except TokenError:
            return Response({"error": "유효하지 않은 refresh token입니다."}, status=status.HTTP_400_BAD_REQUEST)