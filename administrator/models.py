from django.db import models
from users.models import *
from cases.models import *

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Payment(models.Model):
    client = models.ForeignKey(
        Citizen, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(
        Lawyer, on_delete=models.CASCADE)
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=50)
    signature = models.CharField(max_length=256)
    refund_payment_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=100, choices=[(
        'Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')

    def __str__(self):
        return f"Payment - {self.order_id} for {self.email}"
