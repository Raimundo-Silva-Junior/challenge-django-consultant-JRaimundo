from django.db import models
from functools import partial
from uuid import uuid4


class Proposal(models.Model):
    """Propostas dos possíveis clientes aprovados 
    (os não aprovados não são guardados no banco de dados)"""
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(verbose_name="Nome")
    document = models.JSONField(verbose_name="Documento")
    
    AWAITING = "AWAITING"
    APPROVED = "APPROVED"
    REFUSED = "REFUSED"
    
    STATUS_CHOICES = (
        (AWAITING, "Awaiting"),
        (APPROVED, "Approved"),
        (REFUSED, "Refused"),
    )
    
    status = models.CharField(verbose_name="Status", max_length=10,  choices=STATUS_CHOICES)
    
    def __str__(self):
        return self.name
    
    
class ProposalModel(models.Model):
    """Modelo de proposta
    (A tabela conterá apenas uma query que poderá ser alterada pelo usuário no frontend)"""
    
    proposal_name = models.TextField(
        verbose_name="Model Name",
        default="Modelo de Proposta", 
        auto_created=True
    )
    content = models.JSONField(
        default=partial(dict, CPF="descrição...", IDADE="descrição..."),
        verbose_name="Conteúdo da Proposta"
    )
    
    def __str__(self):
        return self.proposal_name