from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm, UsernameField
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from .models import Usuario


class NovoUsuarioForm(forms.ModelForm):
    primeiro_nome = forms.CharField(max_length=150, required=True,
                                    label='Nome')
    sobrenome = forms.CharField(max_length=150, required=True,
                                label='Sobrenome')
    email = forms.EmailField(required=True)
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super(NovoUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class': 'cpfmask'})
        self.fields['data_nasc'].widget.attrs.update({'class': 'datemask'})

    def clean_cpf(self):
        data = self.cleaned_data['cpf']
        try:
            Usuario.objects.get(cpf=data)
            raise ValidationError('CPF já cadastrado')
        except Usuario.DoesNotExist:
            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            raise ValidationError('Email já cadastrado')
        except User.DoesNotExist:
            return data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    class Meta:
        model = Usuario
        fields = ['primeiro_nome', 'sobrenome', 'email', 'data_nasc', 'cpf',
                  'password1', 'password2']


class DadosComplementaresUsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['rg', 'org_emis_rg', 'est_emis_rg', 'nacionalidade',
                  'naturalidade_cidade', 'naturalidade_estado']


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label='CPF')

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'cpfmask'})
