from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from decimal import Decimal
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count, Max
from .models import Fournisseur, Facture
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from datetime import datetime

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

def factures_par_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    factures = Facture.objects.filter(fournisseur=fournisseur)
    return render(request, 'factures/factures_par_fournisseur.html', {
        'fournisseur': fournisseur,
        'factures': factures
    })
    
def factures_par_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    tous_les_fournisseurs = Fournisseur.objects.all()
    factures = Facture.objects.filter(fournisseur=fournisseur)
    
    # Filtre par période
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    if date_debut and date_fin:
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
            factures = factures.filter(date__range=[date_debut, date_fin])
        except ValueError:
            pass
    
    # Filtre par état
    etat = request.GET.get('etat')
    if etat:
        factures = factures.filter(etat=etat)
    
    # Recherche par numéro
    numero = request.GET.get('numero')
    if numero:
        factures = factures.filter(numero__icontains=numero)
    
    # Pagination
    paginator = Paginator(factures.order_by('-date'), 5)
    page_number = request.GET.get('page')
    factures_page = paginator.get_page(page_number)
    
    # Calcul des totaux (sur les résultats filtrés)
    total_ttc = factures.aggregate(total=Sum('montant_ttc'))['total'] or 0
    total_ht = factures.aggregate(total=Sum('montant'))['total'] or 0
    total_ttc_non_regle = factures.filter(etat='N').aggregate(total=Sum('montant_ttc'))['total'] or 0
    total_ht_non_regle = factures.filter(etat='N').aggregate(total=Sum('montant'))['total'] or 0
    
    context = {
        'fournisseur': fournisseur,
        'factures': factures_page,
        'total_ttc': total_ttc,
        'total_ht': total_ht,
        'total_ttc_non_regle': total_ttc_non_regle,
        'total_ht_non_regle': total_ht_non_regle,
        'fournisseurs': tous_les_fournisseurs, 
    }
    
    return render(request, 'dashboard/factures_par_fournisseur.html', context)

@require_POST
def ajouter_facture(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    numero = request.POST.get('numero')
    date = request.POST.get('date')
    montant = request.POST.get('montant')
    etat = request.POST.get('etat', 'N')
    
    facture = Facture(
        fournisseur=fournisseur,
        numero=numero,
        date=date,
        montant=float(montant),
        etat=etat
    )
    facture.save()  # Les champs retenu et montant_ttc sont calculés automatiquement
    
    return redirect('fournisseur_factures', fournisseur_id=fournisseur_id)

def facture_json(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    data = {
        'id': facture.id,
        'numero': facture.numero,
        'date': facture.date.strftime('%Y-%m-%d'),
        'montant': str(facture.montant),
        'etat': facture.etat,
        'retenu': str(facture.retenu),
        'montant_ttc': str(facture.montant_ttc),
    }
    return JsonResponse(data)

@require_POST
def editer_facture(request):
    facture = get_object_or_404(Facture, id=request.POST.get('id'))
    try:
        facture.numero = request.POST.get('numero')
        facture.date = request.POST.get('date')
        facture.montant = Decimal(request.POST.get('montant'))
        facture.etat = request.POST.get('etat')
        facture.save()
        return redirect('fournisseur_factures', fournisseur_id=facture.fournisseur.id)
    except Exception as e:
        # Gérer l'erreur (ajouter un message d'erreur si nécessaire)
        return redirect('fournisseur_factures', fournisseur_id=facture.fournisseur.id)
    
@require_POST
def supprimer_facture(request):
    facture = get_object_or_404(Facture, id=request.POST.get('facture_id'))
    fournisseur_id = facture.fournisseur.id
    facture.delete()
    
    return redirect('fournisseur_factures', fournisseur_id=fournisseur_id)