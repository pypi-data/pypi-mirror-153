
"""This module is loaded by DjangoLDP core during setup."""

# define an extra variable (should be prefix with package name)
MYPACKAGE_VAR = 'MY_DEFAULT_VAR'

# register an extra middleware
MIDDLEWARE = []

REGISTRATION_USER_FORM = 'djangoldp_hiphopcommunity.forms.HipHopUserForm'
REGISTRATION_TEMPLATE_PATH = 'hiphopcommunity/registration_form.html'
