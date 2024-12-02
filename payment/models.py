from django.db import models
from django.conf import settings
from tourism.models import Tour

class Payment(models.Model):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    PENDING = 'PENDING'

    PAYMENT_STATUS_CHOICES = [
        (SUCCESS, 'Successful'),
        (FAILED, 'Failed'),
        (PENDING, 'Pending')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who made the payment
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)  # The tour for which payment was made
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount the user paid
    ref_id = models.CharField(max_length=100)  # Zarinpal reference ID
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default=FAILED,
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of payment

    def __str__(self):
        return f"Payment {self.ref_id} for {self.user.username} on {self.tour.title}"