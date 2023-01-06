from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['ACCESS_TOKEN_LIFETIME'] = int(api_settings.ACCESS_TOKEN_LIFETIME.seconds)
        data['REFRESH_TOKEN_LIFETIME'] = int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds())
        data['AUTH_HEADER_TYPES'] = api_settings.AUTH_HEADER_TYPES

        # data['user'] = {
        #     'username': self.user.get_username(),
        #     'groups': self.user.groups.values_list('name', flat=True)
        # }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data