from rest_framework import serializers
from app.settings import GOOGLE_CLIENT_ID
from . import google, facebook
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            avatar = user_data['picture']['data']['url']
            provider = 'facebook'

            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                avatar=avatar,
            )
        except Exception:
            raise serializers.ValidationError('The token  is invalid or expired. Please login again.')


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    @staticmethod
    def validate_auth_token(auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']

        except Exception:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        avatar_google = user_data['picture']

        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id,
            email=email, first_name=first_name,
            last_name=last_name, avatar=avatar_google)
