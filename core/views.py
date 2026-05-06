from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail

from .models import Vaga, Curriculo, Candidatura
from .forms import VagaForm, CurriculoForm, CadastroUsuarioForm


User = get_user_model()

# Create your views here.
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Você não tem permissão para acessar essa página.'
        )
        return redirect('lista-vagas')


class VagaListView(ListView):
    model = Vaga
    template_name = 'core/vagas/lista.html'
    context_object_name = 'vagas'
    paginate_by = 6

    def get_queryset(self):
        queryset = Vaga.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(ativa=True)

        busca = self.request.GET.get('busca')
        ordenar = self.request.GET.get('ordenar')

        if busca:
            queryset = queryset.filter(
                Q(titulo__icontains=busca) |
                Q(empresa__icontains=busca) |
                Q(cidade__icontains=busca) |
                Q(modalidade__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(requisitos__icontains=busca)
            )

        if ordenar == 'antigas':
            queryset = queryset.order_by('data_publicacao')
        elif ordenar == 'menor_salario':
            queryset = queryset.order_by('salario')
        elif ordenar == 'maior_salario':
            queryset = queryset.order_by('-salario')
        else:
            queryset = queryset.order_by('-data_publicacao')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidaturas_ids = []

        if self.request.user.is_authenticated:
            curriculo = Curriculo.objects.filter(usuario=self.request.user).first()

            if curriculo:
                candidaturas_ids = list(
                    Candidatura.objects.filter(curriculo=curriculo)
                    .values_list('vaga_id', flat=True)
                )

        context['candidaturas_ids'] = candidaturas_ids
        return context


class VagaCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'core/vagas/formulario.html'
    success_url = reverse_lazy('lista-vagas')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Vaga cadastrada com sucesso!')
        return super().form_valid(form)


class VagaUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'core/vagas/formulario.html'
    success_url = reverse_lazy('lista-vagas')

    def form_valid(self, form):
        messages.success(self.request, 'Vaga atualizada com sucesso!')
        return super().form_valid(form)


class VagaDetailView(DetailView):
    model = Vaga
    template_name = 'core/vagas/detalhe.html'
    context_object_name = 'vaga'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidatura = None
        candidaturas_da_vaga = []

        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                candidaturas_da_vaga = Candidatura.objects.filter(
                    vaga=self.object
                ).select_related('curriculo', 'curriculo__usuario')
            else:
                curriculo = Curriculo.objects.filter(usuario=self.request.user).first()

                if curriculo:
                    candidatura = Candidatura.objects.filter(
                        vaga=self.object,
                        curriculo=curriculo
                    ).first()

        context['candidatura'] = candidatura
        context['candidaturas_da_vaga'] = candidaturas_da_vaga
        return context


class VagaDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Vaga
    template_name = 'core/vagas/confirmar_exclusao.html'
    success_url = reverse_lazy('lista-vagas')

    def form_valid(self, form):
        messages.success(self.request, 'Vaga excluída com sucesso!')
        return super().form_valid(form)


class MeuCurriculoView(LoginRequiredMixin, TemplateView):
    template_name = 'core/curriculos/meu_curriculo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curriculo'] = Curriculo.objects.filter(usuario=self.request.user).first()
        return context


class CurriculoCreateView(LoginRequiredMixin, CreateView):
    model = Curriculo
    form_class = CurriculoForm
    template_name = 'core/curriculos/formulario.html'
    success_url = reverse_lazy('meu-curriculo')

    def dispatch(self, request, *args, **kwargs):
        if Curriculo.objects.filter(usuario=request.user).exists():
            messages.warning(request, 'Você já possui um currículo cadastrado.')
            return redirect('meu-curriculo')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Currículo cadastrado com sucesso!')
        return super().form_valid(form)


class CurriculoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curriculo
    form_class = CurriculoForm
    template_name = 'core/curriculos/formulario.html'
    success_url = reverse_lazy('meu-curriculo')

    def get_queryset(self):
        return Curriculo.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        curriculo = form.instance

        if form.cleaned_data.get('remover_pdf') and curriculo.arquivo_pdf:
            curriculo.arquivo_pdf.delete(save=False)
            curriculo.arquivo_pdf = None

        messages.success(self.request, 'Currículo atualizado com sucesso!')
        return super().form_valid(form)


class CurriculoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curriculo
    template_name = 'core/curriculos/confirmar_exclusao.html'
    success_url = reverse_lazy('meu-curriculo')

    def get_queryset(self):
        return Curriculo.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Currículo excluído com sucesso!')
        return super().form_valid(form)


class CurriculoRemoverPdfView(LoginRequiredMixin, View):
    def post(self, request, pk):
        curriculo = Curriculo.objects.filter(pk=pk, usuario=request.user).first()

        if curriculo and curriculo.arquivo_pdf:
            curriculo.arquivo_pdf.delete(save=False)
            curriculo.arquivo_pdf = None
            curriculo.save()
            messages.success(request, 'Arquivo PDF removido com sucesso!')
        else:
            messages.warning(request, 'Nenhum arquivo PDF encontrado para remover.')

        return redirect('meu-curriculo')


class CandidatarVagaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vaga = get_object_or_404(Vaga, pk=pk, ativa=True)
        curriculo = Curriculo.objects.filter(usuario=request.user).first()

        if not curriculo:
            messages.warning(request, 'Você precisa cadastrar um currículo antes de se candidatar.')
            return redirect('meu-curriculo')

        candidatura_existente = Candidatura.objects.filter(
            vaga=vaga,
            curriculo=curriculo
        ).exists()

        if candidatura_existente:
            messages.warning(request, 'Você já se candidatou a esta vaga.')
            return redirect('detalhe-vaga', pk=pk)

        Candidatura.objects.create(
            vaga=vaga,
            curriculo=curriculo
        )

        send_mail(
            subject='Confirmação de candidatura',
            message=f'Olá, {curriculo.nome_completo}! Sua candidatura para a vaga {vaga.titulo} foi enviada com sucesso.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

        messages.success(request, 'Candidatura enviada com sucesso!')
        return redirect('minhas-candidaturas')


class MinhasCandidaturasView(LoginRequiredMixin, ListView):
    model = Candidatura
    template_name = 'core/candidaturas/minhas_candidaturas.html'
    context_object_name = 'candidaturas'
    paginate_by = 6

    def get_queryset(self):
        return Candidatura.objects.filter(
            curriculo__usuario=self.request.user
        ).select_related('vaga', 'curriculo')


class RemoverCandidaturaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        candidatura = Candidatura.objects.filter(
            pk=pk,
            curriculo__usuario=request.user
        ).first()

        if candidatura:
            candidatura.delete()
            messages.success(request, 'Candidatura removida com sucesso!')
        else:
            messages.warning(request, 'Candidatura não encontrada.')

        return redirect('minhas-candidaturas')


class CadastroUsuarioView(CreateView):
    model = User
    form_class = CadastroUsuarioForm
    template_name = 'registration/cadastro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso! Agora você pode fazer login.')
        return super().form_valid(form)