from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseurs_view, name='fournisseurs'),
    path('fournisseurs/add/', views.add_fournisseur, name='add_fournisseur'),
    path('fournisseurs/<int:id>/edit/', views.edit_fournisseur, name='edit_fournisseur'),
    path('fournisseurs/<int:id>/delete/', views.delete_fournisseur, name='delete_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/factures/', views.factures_par_fournisseur, name='fournisseur_factures'),
    path('ajouter/<int:fournisseur_id>/', views.ajouter_facture, name='ajouter_facture'),
    path('factures/<int:facture_id>/json/', views.facture_json, name='facture_json'),
    path('editer/', views.editer_facture, name='editer_facture'),
    path('supprimer/', views.supprimer_facture, name='supprimer_facture'),
]