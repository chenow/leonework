from django.db import models
from companies.models import Company


class Offer(models.Model):
    name = models.CharField(max_length=200)
    offer_id = models.CharField(max_length=200, unique=True)
    price_id = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.price}€"

    class Meta:
        ordering = ["price"]
        verbose_name_plural = "Offres du site"
        verbose_name = "Offre"


class Subscription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    # type : ignore
    PAYMNENT_CHOICES = [
        ["Payement initialisé", "initialised"],
        ["Payement reçu", "success"],
        ["Payement en attente", "waiting"],
        ["Payement échoué", "error"],
    ]
    payment_status = models.CharField(
        choices=PAYMNENT_CHOICES,  # type: ignore
        default="initialised",
        max_length=20,
    )

    def __str__(self) -> str:
        return f"{self.company.name} - {self.offer.name}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Achats des entreprises du site"
        verbose_name = "Achat"
