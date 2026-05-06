from django.db import models
from django.conf import settings

# Create your models here.
class Vaga(models.Model):
    MODALIDADE_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    titulo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)

    modalidade = models.CharField(
        max_length=20,
        choices=MODALIDADE_CHOICES
    )

    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    descricao = models.TextField()
    requisitos = models.TextField()

    ativa = models.BooleanField(default=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vagas_criadas'
    )

    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo


class Curriculo(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    formacao = models.CharField(max_length=150)
    experiencia = models.TextField()
    arquivo_pdf = models.FileField(upload_to='curriculos/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


class Candidatura(models.Model):
    STATUS_CHOICES = [
        ('enviada', 'Enviada'),
        ('analise', 'Em análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE, related_name='candidaturas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enviada')
    data_candidatura = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vaga', 'curriculo'], name='unique_candidatura')
        ]
        ordering = ['-data_candidatura']

    def __str__(self):
        return f'{self.curriculo.nome_completo} se candidatou para {self.vaga.titulo}'