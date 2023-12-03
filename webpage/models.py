from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count
from django.contrib.auth.models import User

class Beer(models.Model):
    author = models.CharField(max_length=25)
    published_date = models.DateField(default=timezone.now)
    brewery = models.CharField(max_length=25)
    name = models.CharField(max_length=30)
    style = models.CharField(max_length=25)
    alcohol_content = models.FloatField(default=0)
    blg = models.FloatField(default=0)
    picture = models.CharField(max_length=250, null=True, blank=True)
    # Only Beers approved by admin should be shown in the Beer Ranking page - default False
    isapproved = models.BooleanField(default=False)

    # Function that set isapproved to True - Beer is shown in the Beer Ranking
    def approve(self):
        self.isapproved = True
        self.save()

    # Function that returns calculated average from users rating
    def reviews_avg(self):
        # Filter - only reviews of selected beer are considered, then aggregation
        # and usage of Avg which calculates average
        review = Review.objects.filter(beer=self).aggregate(average=Avg('score'))
        avg = 0
        if review["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(review["average"]), 1)
        return avg

    # Function that returns the total number of reviews (ratings)
    # The same principle as in previous function
    def reviews_counter(self):
        reviews = Review.objects.filter(beer=self).aggregate(count=Count('pk'))
        counter = 0
        if reviews["count"] is not None:
            counter = int(reviews["count"])
        return counter

    def __str__(self):
        return self.name

# Users can rate and add comment to each beer in the database.
class Review(models.Model):
    # Each review must be assigned to the beer that it applies to
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(max_length=250, null=True, blank=True)
    published_date = models.DateField(default=timezone.now)
    banned = models.BooleanField(default=False)
