from django.shortcuts import render

from django.shortcuts import render
from .models import Fournisseur

def fournisseurs_view(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'dashboard/fournisseurs.html', {'fournisseurs': fournisseurs})