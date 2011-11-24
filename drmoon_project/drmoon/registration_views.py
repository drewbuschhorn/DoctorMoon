from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,get_backends
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))
    first_name = forms.CharField(label=_("First Name"),max_length=30,help_text=_("Optional. Enter your first name."),required=False)
    last_name = forms.CharField(label=_("Last Name"),max_length=30,help_text=_("Optional. Enter your last name."),required=False)
    email = forms.EmailField(label=_("Email Address"), max_length=75,help_text=_("Required. Must contain a valid email address."))


    class Meta:
        model = User
        fields = ("username","password1","password2","email","first_name","last_name")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

def register(request):
    form = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return _authAndLogInNewUser(new_user,request)
    
    if form is None:
        form = UserCreationForm()

    return render_to_response("registration/register.html", {
         'form': form,
        }, RequestContext(request))

def _authAndLogInNewUser(user,request):
    
    if user is not None:
        if user.is_active:
	    backend = get_backends()[0]
            user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            login(request, user)
            return HttpResponseRedirect("/networkgraphs/index")

    return HttpResponseRedirect("/accounts/registration")
