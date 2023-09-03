import requests
from celery import shared_task

@shared_task(broker="redis://redis:6379/0")
def verify_proposal_task(data):
    """Celery task que verifica a proposta de crédito."""
    
    response = requests.post(
        url="https://loan-processor.digitalsys.com.br/api/v1/loan/",
        json=data,
    )
    
    return response.json()["approved"]