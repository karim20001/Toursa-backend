from django.db import models
from django.conf import settings

class Tour(models.Model):
    TRANSPORTATION_CHOICES = [
        ('اتوبوس', 'اتوبوس'),
        ('قطار', 'قطار'),
        ('پرواز داخلی', 'پرواز داخلی'),
        ('پرواز خارجی', 'پرواز خارجی'),
    ]

    title = models.CharField(max_length=200)  # Title of the tour
    origin_city = models.CharField(max_length=100)
    origin_country = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    days_of_tour = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    remaining_capacity = models.PositiveIntegerField()
    transportation_type = models.CharField(max_length=20, choices=TRANSPORTATION_CHOICES)
    price = models.IntegerField()
    price_off = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Optional description
    is_available = models.BooleanField(default=True)  # To mark if the tour is available or sold out
    cover_photo = models.ImageField(upload_to='tour_photos/', blank=True, null=True)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)  # Automatically set when purchased
    payment_status = models.CharField(max_length=20, choices=[("PAID", "Paid"), ("PENDING", "Pending")], default="PAID")

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"
