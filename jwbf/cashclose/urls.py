from django.urls import path
from django.conf.urls import include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('statements/', views.StatementListView.as_view(), name='statements'),
    path('statements/<int:pk>', views.StatementDetailView.as_view(), name='statement-detail'),

]