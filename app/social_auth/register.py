from django.contrib.auth import authenticate

from register.models import User
from app.settings import SOCIAL_SECRET
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, first_name, last_name, avatar):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            # registered_user = authenticate(email=email, password=SOCIAL_SECRET)

            return User.objects.get(email=email).tokens()

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            f'avatar_{provider}': avatar,
            'password': SOCIAL_SECRET}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.is_active = True
        user.auth_provider = provider
        user.save()
        #authenticate(email=email, password=SOCIAL_SECRET)
        return user.tokens()
