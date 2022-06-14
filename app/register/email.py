import string
import random
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage
from django.template.loader import get_template
from djoser import utils
from djoser.conf import settings
from app.settings import EMAIL_HOST_USER, DOMAIN

# generate random digits by length 6
random_digits = ''.join(random.choice(string.digits) for _ in range(6))


# override djoser implementation for Password Reset Email
class PasswordResetEmail(BaseEmailMessage):
    template_name = "register/reset_password.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["random_digits"] = random_digits
        # print(context)
        return context

    def send(self, to, *args, **kwargs):
        self.render()
        self.subject = 'Password reset on ' + DOMAIN
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email', EMAIL_HOST_USER
        )

        ctx = {
            'site_name': DOMAIN,
            'protocol': self.get_context_data().get('protocol'),
            'uid': self.get_context_data().get('uid'),
            'token': self.get_context_data().get('token'),
            'random_digits': random_digits,
            'email': self.context.get('user'),
        }
        html_content = get_template('register/reset_password.html').render(ctx)
        self.attach_alternative(html_content, "text/html")
        super(BaseEmailMessage, self).send(*args, **kwargs)


# override djoser implementation for Activation Email
class ActivationEmail(BaseEmailMessage):
    template_name = "register/activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context

    def send(self, to, *args, **kwargs):
        self.render()
        self.subject = 'Account activation on ' + DOMAIN
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email', EMAIL_HOST_USER
        )

        ctx = {
            'site_name': DOMAIN,
            'protocol': self.get_context_data().get('protocol'),
            'uid': self.get_context_data().get('uid'),
            'token': self.get_context_data().get('token'),
            'email': self.context.get('user'),
        }
        html_content = get_template('register/activation.html').render(ctx)
        self.attach_alternative(html_content, "text/html")
        super(BaseEmailMessage, self).send(*args, **kwargs)


# override djoser implementation for Confirmation Email
class ConfirmationEmail(BaseEmailMessage):
    template_name = "register/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["first_name"] = user.first_name
        context["last_name"] = user.last_name
        return context

    def send(self, to, *args, **kwargs):
        self.render()
        self.subject = DOMAIN + '- Your account has been successfully created and activated!'
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email', EMAIL_HOST_USER
        )

        ctx = {
            'site_name': DOMAIN,
            'email': self.context.get('user'),
            'first_name': self.get_context_data().get('first_name'),
            'last_name': self.get_context_data().get('last_name'),
        }
        html_content = get_template('register/confirmation.html').render(ctx)
        self.attach_alternative(html_content, "text/html")
        super(BaseEmailMessage, self).send(*args, **kwargs)


# override djoser implementation for Password Changed Confirmation Email
class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "register/password_changed.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["first_name"] = user.first_name
        context["last_name"] = user.last_name
        return context

    def send(self, to, *args, **kwargs):
        self.render()
        self.subject = DOMAIN + '- Your password has been successfully changed!'
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email', EMAIL_HOST_USER
        )

        ctx = {
            'site_name': DOMAIN,
            'email': self.context.get('user'),
            'first_name': self.get_context_data().get('first_name'),
            'last_name': self.get_context_data().get('last_name'),
        }
        html_content = get_template('register/password_changed.html').render(ctx)
        self.attach_alternative(html_content, "text/html")
        super(BaseEmailMessage, self).send(*args, **kwargs)
