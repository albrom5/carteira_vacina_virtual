from bootstrap_modal_forms.forms import BSModalModelForm

from apps.vacina.models import Aplicacao


class RegistraAplicacaoForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistraAplicacaoForm, self).__init__(*args, **kwargs)
        self.fields['data_aplicacao'].widget.attrs.update(
            {'class': 'form-control datemask'}
        )
        self.fields['dose'].widget.attrs.update(
            {'class': 'form-select'}
        )
        self.fields['local'].widget.attrs.update(
            {'class': 'form-select'}
        )

    class Meta:
        model = Aplicacao
        fields = ['dose', 'local', 'data_aplicacao']

