from django.db import models


class Donation(models.Model):
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name  = models.CharField(max_length=100)
    email       = models.EmailField()
    postcode    = models.CharField(blank=True, null=True, max_length=20)
    message     = models.TextField(blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"

