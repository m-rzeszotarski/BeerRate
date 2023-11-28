from django.conf import settings
from django.db import models
from django.utils import timezone

class Beer(models.Model):

    author = models.CharField(max_length=25)
    published_date = models.DateField(default=timezone.now)
    brewery = models.CharField(max_length=25)
    name = models.CharField(max_length=30)
    style = models.CharField(max_length=25)
    alcohol_content = models.FloatField(default=0)
    blg = models.FloatField(default=0)
    isapproved = models.BooleanField(default=False)

    def approve(self):
        self.isapproved = True
        self.save()

    def __str__(self):
        return self.name
