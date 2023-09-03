from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProposalModelSerializer, ProposalSerializer
from .models import ProposalModel, Proposal
from .tasks import verify_proposal_task


class ProposalSendDataView(viewsets.ModelViewSet):
    """View Responsável por enviar a proposta no banco de dados caso a proposta seja aprovada."""
    
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.all()
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):

        task = verify_proposal_task(request.data)
        
        if task:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=500, data={"Error": "Invalid Proposal"})
    
    
class ProposalDataView(viewsets.ModelViewSet):
    """View Responsável pelas propostas de todos os clientes."""
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.all()
    http_method_names = ('get', "put", "delete")


class ProposalModelChangeView(viewsets.ModelViewSet):
    """View Responsável por alterar o modelo de proposta."""
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProposalModelSerializer
    queryset = ProposalModel.objects.filter(id=1)
    http_method_names = ('put',)
    
    
class ProposalModelGetView(viewsets.ModelViewSet):
    """View Responsável por pegar o modelo de proposta."""
    serializer_class = ProposalModelSerializer
    queryset = ProposalModel.objects.filter(id=1)
    http_method_names = ('get',)
    
    
