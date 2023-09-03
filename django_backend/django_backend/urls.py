"""django_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import ProposalModelChangeView, ProposalModelGetView, ProposalSendDataView, ProposalDataView


route = routers.DefaultRouter()

route.register("api/proposal_model/change", ProposalModelChangeView, basename="Proposal Model Change")
route.register("api/proposal_model/get", ProposalModelGetView, basename="Proposal Model Get")
route.register("api/proposal/send", ProposalSendDataView, basename="Proposal send")
route.register("api/proposal/data", ProposalDataView, basename="Proposal Data")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", TokenObtainPairView.as_view()),
    path("api/token-refresh/", TokenRefreshView.as_view()),
    path("", include(route.urls))
]
