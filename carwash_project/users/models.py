from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE = [
        ('client', 'Client'),
        ('cleaner', 'Nettoyeur'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    cleaner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pending','En attente'), ('confirmed','Confirmé'), ('done','Terminé')])
    location = models.TextField()

    def __str__(self):
        return f"{self.client.username} - {self.date}"
