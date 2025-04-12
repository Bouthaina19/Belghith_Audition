from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Max
from .models import Fournisseur

def fournisseurs_view(request):
    fournisseurs = Fournisseur.objects.annotate(
        total_factures=Count('factures'),  # Utilisez le related_name exact
        derniere_facture=Max('factures__date')  # Même related_name ici
    )
    return render(request, 'dashboard/fournisseurs.html', {'fournisseurs': fournisseurs})

def add_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        if nom:
            Fournisseur.objects.create(nom=nom)
            messages.success(request, 'Fournisseur ajouté avec succès')
        return redirect('fournisseurs')
    return redirect('fournisseurs')

def edit_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        if nom:
            fournisseur.nom = nom
            fournisseur.save()
            messages.success(request, 'Fournisseur mis à jour avec succès')
        return redirect('fournisseurs')
    return redirect('fournisseurs')

def delete_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, 'Fournisseur supprimé avec succès')
    return redirect('fournisseurs')