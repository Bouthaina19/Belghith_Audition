from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseurs_view, name='fournisseurs'),
    path('fournisseurs/add/', views.add_fournisseur, name='add_fournisseur'),
    path('fournisseurs/<int:id>/edit/', views.edit_fournisseur, name='edit_fournisseur'),
    path('fournisseurs/<int:id>/delete/', views.delete_fournisseur, name='delete_fournisseur'),
]