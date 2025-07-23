from django.db import models
import uuid


# Uma classe para criar data de criação e atualização em todos os modelos
class TimeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Nao cria tabela


# Classe de profissional, seguindo as regras de negócio
class Profissional(TimeStampeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_social = models.CharField(max_length=255)
    profissao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=500)
    contato = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_social


# Classe de consulta, com uma consulta para cada profissional
class Consulta(TimeStampeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="consultas"
    )
    data_consulta = models.DateTimeField()

    def __str__(self):
        return f"Consulta de {self.profissional.nome_social} em {
            self.data_consulta.strftime('%d %m %Y às %H:%M')}"
