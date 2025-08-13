# emissions/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Action(models.Model):
    ACTION_CHOICES = [
        ('bike', 'Used Bicycle'),
        ('plant', 'Planted a Tree'),
        ('public_transport', 'Used Public Transport'),
        ('no_plastic', 'Avoided Plastic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    co2_saved_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.co2_saved_kg} kg"

class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'co2_saved_kg', 'date')
    list_filter = ('action_type', 'date')
    search_fields = ('user__username',)


class EmissionLog(models.Model):
    CATEGORY_CHOICES = [
        ('travel', 'Travelled Responsibly'),
        ('energy', 'Saved Energy'),
        ('food', 'Ate Sustainably'),
        ('waste', 'Managed Waste'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.FloatField()  # e.g. km, kWh, kg
    emitted = models.FloatField(default=0)  # kg CO2 actually emitted
    saved = models.FloatField(default=0)    # kg CO2 saved
    date_logged = models.DateTimeField(auto_now_add=True)