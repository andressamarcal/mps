# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from app import views

from .views import CSVCreateView, DashboardView, ReportView, GraphView

urlpatterns = [

    path('', login_required(DashboardView.as_view()), name='home'),
    path('upload/', login_required(CSVCreateView.as_view()), name='upload'),
    path('report/', login_required(ReportView.as_view()), name='report'),
    # path('graph/', login_required(views.graph), name='graph'),
    path('graph/', login_required(GraphView.as_view()), name='graph'),
    
    re_path(r'^.*\.*', views.pages, name='pages'),

]
