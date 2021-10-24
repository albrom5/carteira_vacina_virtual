from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm, UsernameField
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from localflavor.br.br_states import STATE_CHOICES

from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Usuario, Cidade, Telefone, Endereco


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
    refund_dict = {value: key for key, value in STATE_CHOICES}
    siglas = [('', '----')]
    for key, value in refund_dict.items():
        siglas.append((value, value))
    estado_natural = forms.ChoiceField(choices=siglas,
                                       label='Naturalidade', required=False)
    est_emis_rg = forms.ChoiceField(choices=siglas,
                                       label='Estado emissor do RG', required=False)
    def __init__(self, *args, **kwargs):
        super(DadosComplementaresUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['naturalidade_cidade'].queryset = Cidade.objects.none()
        self.fields['naturalidade_cidade'].widget.attrs.update(
            {'class': 'form-select'}
        )
        self.fields['estado_natural'].widget.attrs.update(
            {'class': 'form-select'}
        )
        self.fields['est_emis_rg'].widget.attrs.update(
            {'class': 'form-select'}
        )

        if 'estado_natural' in self.data:
            try:
                estado = self.data.get('estado_natural')
                self.fields[
                    'naturalidade_cidade'].queryset = Cidade.objects.filter(
                    state=estado).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            estado = self.instance.naturalidade_cidade.state
            self.fields['estado_natural'].initial = estado
            self.fields[
                'naturalidade_cidade'].queryset = Cidade.objects.filter(
                    state=estado).order_by('name')

    class Meta:
        model = Usuario
        fields = ['rg', 'org_emis_rg', 'est_emis_rg', 'nacionalidade',
                  'naturalidade_cidade']


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label='CPF')

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'cpfmask'})


class TelefoneForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super(TelefoneForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs.update(
            {'class': 'form-control telmask'}
        )
        self.fields['principal'].widget.attrs.update(
            {'class': 'form-check-input'}
        )

    class Meta:
        model = Telefone
        fields = ['numero', 'principal']


class EnderecoForm(BSModalModelForm):
    refund_dict = {value: key for key, value in STATE_CHOICES}
    siglas = [('', '----')]
    for key, value in refund_dict.items():
        siglas.append((value, value))
    estado = forms.ChoiceField(choices=siglas,
                               label='Estado', required=False)
    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        self.fields['principal'].widget.attrs.update(
            {'class': 'form-check-input'}
        )
        self.fields['cep'].widget.attrs.update(
            {'class': 'cep cepmask form-control'})
        self.fields['logradouro'].widget.attrs.update(
            {'class': 'rua form-control'})
        self.fields['bairro'].widget.attrs.update(
            {'class': 'bairro form-control'})
        self.fields['ender_num'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['ender_compl'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['cidade'].widget.attrs.update(
            {'class': 'cidade form-control'})
        self.fields['estado'].widget.attrs.update(
            {'class': 'uf form-select'})

    class Meta:
        model = Endereco
        fields = ['cep', 'logradouro', 'ender_num', 'ender_compl',
                  'bairro', 'cidade', 'estado', 'principal']
