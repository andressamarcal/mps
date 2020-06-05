# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from app import views

from .views import CSVCreateView, DashboardView, ReportView

urlpatterns = [

    path('', login_required(DashboardView.as_view()), name='home'),
    path('upload/', login_required(CSVCreateView.as_view()), name='upload'),
    path('report/', login_required(ReportView.as_view()), name='report'),
    
    re_path(r'^.*\.*', views.pages, name='pages'),
]