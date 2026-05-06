from django.urls import path
from .views import (
    VagaListView,
    VagaDetailView,
    VagaCreateView,
    VagaUpdateView,
    VagaDeleteView,
    MeuCurriculoView,
    CurriculoCreateView,
    CurriculoUpdateView,
    CurriculoDeleteView,
    CurriculoRemoverPdfView,
    CandidatarVagaView,
    MinhasCandidaturasView,
    RemoverCandidaturaView,
    CadastroUsuarioView,
)

urlpatterns = [
    path('', VagaListView.as_view(), name='lista-vagas'),
    path('vaga/<int:pk>/', VagaDetailView.as_view(), name='detalhe-vaga'),
    path('vaga/nova/', VagaCreateView.as_view(), name='criar-vaga'),
    path('vaga/<int:pk>/editar/', VagaUpdateView.as_view(), name='editar-vaga'),
    path('vaga/<int:pk>/excluir/', VagaDeleteView.as_view(), name='excluir-vaga'),

    path('meu-curriculo/', MeuCurriculoView.as_view(), name='meu-curriculo'),
    path('meu-curriculo/novo/', CurriculoCreateView.as_view(), name='criar-curriculo'),
    path('meu-curriculo/<int:pk>/editar/', CurriculoUpdateView.as_view(), name='editar-curriculo'),
    path('meu-curriculo/<int:pk>/excluir/', CurriculoDeleteView.as_view(), name='excluir-curriculo'),
    path('meu-curriculo/<int:pk>/remover-pdf/', CurriculoRemoverPdfView.as_view(), name='remover-pdf'),

    path('vaga/<int:pk>/candidatar/', CandidatarVagaView.as_view(), name='candidatar-vaga'),
    path('minhas-candidaturas/', MinhasCandidaturasView.as_view(), name='minhas-candidaturas'),
    path('candidatura/<int:pk>/remover/', RemoverCandidaturaView.as_view(), name='remover-candidatura'),

    path('cadastro/', CadastroUsuarioView.as_view(), name='cadastro'),
]