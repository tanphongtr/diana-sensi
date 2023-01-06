from rest_framework.authtoken import views
from rest_framework import status, generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

class TokenRefreshAPIView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Auth'],
        operation_description='',
        operation_id='Token Refresh',
        operation_summary='',
        responses={
            # 200: AuthSerializer(),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenVerifyAPIView(TokenVerifyView):
    @swagger_auto_schema(
        tags=['Auth'],
        operation_description='',
        operation_id='Token Verify',
        operation_summary='',
        responses={
            # 200: AuthSerializer(),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AuthAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    @swagger_auto_schema(
        tags=['Auth'],
        operation_description='',
        operation_id='Login',
        operation_summary='',
        responses={
            # 200: AuthSerializer(),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
