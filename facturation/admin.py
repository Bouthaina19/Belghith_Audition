from django.contrib import admin
from .models import Fournisseur, Facture

admin.site.register(Fournisseur)
admin.site.register(Facture)