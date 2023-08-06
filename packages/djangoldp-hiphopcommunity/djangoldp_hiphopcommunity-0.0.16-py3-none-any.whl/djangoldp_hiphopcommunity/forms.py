from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
from djangoldp_hiphopcommunity.models import HipHopUserSettings


class HipHopUserForm(RegistrationForm):
    choice=forms.CharField(max_length=50) # the choice of subscription

    class Meta(RegistrationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'choice')


def user_created(sender, user, request, **kwargs):
    form = HipHopUserForm(request.POST)
    data = HipHopUserSettings(user=user, choice=form.data["choice"])
    data.save()

from django_registration.signals import user_registered
user_registered.connect(user_created)
