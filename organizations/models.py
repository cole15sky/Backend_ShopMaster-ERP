from django.db import models
from django.utils import timezone
from datetime import timedelta


class Organization(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, related_name="owned_organizations",null=True, blank=True)
    is_trial = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    @property
    def trial_days_remaining(self):
        remaining = self.trial_ends_at - timezone.now()
        return max(remaining.days, 0)

    @property
    def trial_expired(self):
        return timezone.now() > self.trial_ends_at