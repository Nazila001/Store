from django.shortcuts import render
from django.urls import reverse
from django import views
from . import forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import models


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + "0"


#activation_token_genertaor TokenGenerator()


class SignUpView(views.View):
    def get(self, request):
        form = forms.SignupForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = False
            obj.save()
            subject = 'Please activate your account'
            uid = urlsafe_base64_encode(force_bytes(str(obj.pk)))
            hash = activation_token_genertaor.make_token(obj)
            url = reverse('account:activate', kwargs={'uid': uid,
                                                      'hash': hash})
            domain = get_current_site(request)
            link = f'http://{domain}{url}'

            body = render_to_string('account/signup_email.html', {'obj': obj, 'link': link})
            to = obj.email
            email = EmailMessage(subject, body, 'noreply@store.com', to)
            email.send()
            return render(request, 'account/signup_done.html', {'obj': obj})
        return render(request, 'account/signup.html', {'form': form})


class ActivateView(views.View):
    def get(self, request, uid, hash):
        id = force_str(urlsafe_base64_encode(uid))
        try:
            user = models.User.objects.get(id=id)
            if user.is_active:
                return render(request, 'account/activate_error.html')

        except models.User.DoesNotExist:
            return render(request, 'account/activate_error.html')

        if activation_token_generator.check_token(user, hash):
            user.is_active = True
            user.save()
            return render(request, 'account/activate_done.html')
        return render(request, 'account/activate_error.html')
