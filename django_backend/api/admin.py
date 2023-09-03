from django.contrib import admin
from .models import Proposal, ProposalModel

admin.site.register([Proposal, ProposalModel])
