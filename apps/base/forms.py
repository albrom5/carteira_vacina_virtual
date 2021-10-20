from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from .models import Usuario


class NovoUsuarioForm(forms.ModelForm):
    primeiro_nome = forms.CharField(max_length=150, required=True,
                                    label='Nome')
    sobrenome = forms.CharField(max_length=150, required=True,
                                label='Sobrenome')
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput)

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

    class Meta:
        model = Usuario
        fields = ['primeiro_nome', 'sobrenome', 'email', 'senha', 'data_nasc',
                  'cpf', 'rg', 'org_emis_rg', 'est_emis_rg']
