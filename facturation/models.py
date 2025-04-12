from django.db import models
from django.core.validators import MinValueValidator

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"


class Facture(models.Model):
    ETAT_CHOICES = [
        ('R', 'Réglée'),
        ('N', 'Non réglée'),
    ]

    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="factures")
    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro de facture")
    date = models.DateField(verbose_name="Date de facturation")
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Montant HT"
    )
    retenu = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    etat = models.CharField(max_length=1, choices=ETAT_CHOICES, default='N')

    def __str__(self):
        return f"Facture {self.numero} - {self.fournisseur.nom}"

    def save(self, *args, **kwargs):
        self.retenu = self.montant * 0.01 if self.montant >= 1000 else 0
        self.montant_ttc = self.montant + self.retenu
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ["-date"]