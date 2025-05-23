from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Utilisateur')
    )
    phone = models.CharField(
        _('Téléphone'),
        max_length=20,
        blank=True,
        null=True
    )
    email_verified = models.BooleanField(
        _('Email vérifié'),
        default=False
    )

    class Meta:
        verbose_name = _('Profil utilisateur')
        verbose_name_plural = _('Profils utilisateurs')

    def __str__(self):
        return f"Profil de {self.user.username}"


class Washer(models.Model):
    name = models.CharField(_('Nom'), max_length=100)
    rating = models.DecimalField(
        _('Note'),
        max_digits=3,
        decimal_places=1,
        default=5.0
    )

    class Meta:
        verbose_name = _('Laveur')
        verbose_name_plural = _('Laveurs')

    def __str__(self):
        return self.name


class Car(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name=_('Propriétaire')
    )
    photo = models.ImageField(
        _('Photo'),
        upload_to='car_photos/',
        blank=True,
        null=True
    )
    washer = models.ForeignKey(
        Washer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Laveur attitré')
    )
    service_time = models.PositiveIntegerField(
        _('Durée du service (minutes)'),
        default=30
    )
    service_cost = models.DecimalField(
        _('Coût du service'),
        max_digits=6,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        verbose_name = _('Voiture')
        verbose_name_plural = _('Voitures')
        permissions = [
            ("can_edit_car", _("Peut modifier les informations de la voiture")),
        ]

    def __str__(self):
        return f"Voiture de {self.owner.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Crée ou met à jour le profil utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=instance)