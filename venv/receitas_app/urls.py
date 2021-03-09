from django.urls import path
from . import views

urlpatterns = [
    # criando paths
    path('', views.index, name='index'),
    path('receita', views.receita, name='receita')
]
