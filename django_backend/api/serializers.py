from rest_framework import serializers
from .models import ProposalModel, Proposal


class ProposalSerializer(serializers.ModelSerializer):
    """Serializer para as propostas."""
    
    class Meta:
        model = Proposal
        fields = "__all__"
    
        
class ProposalModelSerializer(serializers.ModelSerializer):
    """Serializer para as o Modelo de proposta."""
    
    class Meta:
        model = ProposalModel
        fields = "__all__"