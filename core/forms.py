from django import forms
from .models import Vaga, Curriculo
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [
            'titulo',
            'empresa',
            'cidade',
            'modalidade',
            'salario',
            'descricao',
            'requisitos',
            'ativa',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
        }


class CurriculoForm(forms.ModelForm):
    remover_pdf = forms.BooleanField(
        required=False,
        label='Remover arquivo PDF atual'
    )

    arquivo_pdf = forms.FileField(
        required=False,
        label='Arquivo do currículo',
        widget=forms.FileInput(attrs={
            'class': 'file-input'
        })
    )

    class Meta:
        model = Curriculo
        fields = [
            'nome_completo',
            'telefone',
            'formacao',
            'experiencia',
            'arquivo_pdf',
        ]


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user