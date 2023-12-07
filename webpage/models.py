from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Users can rate and add comment to each beer in the database.
class Review(models.Model):
    # Each review must be assigned to the Beer or MyBeer that it applies to. I used GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    beer = GenericForeignKey('content_type', 'object_pk')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    hop = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    malt = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    roast = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    smoke = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    fruit = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(max_length=250, null=True, blank=True)
    published_date = models.DateField(default=timezone.now)
    banned = models.BooleanField(default=False)


# Main model - Beer and MyBeer (ecommerce) are inheriting from it
class BeerMain(models.Model):
    author = models.CharField(max_length=25)
    published_date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=30)
    style = models.CharField(max_length=25)
    alcohol_content = models.FloatField(default=0)
    blg = models.FloatField(default=0)
    picture = models.CharField(max_length=250, null=True, blank=True)

    reviews = GenericRelation(Review, content_type_field='content_type', object_id_field='object_pk')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

# Function that returns calculated average from users rating
    def reviews_avg_score(self):
        # Filter - only reviews of selected beer are considered, then aggregation
        # and usage of Avg which calculates average
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('score'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg

        # Function that returns the total number of reviews (ratings)
        # The same principle as in previous function

    def reviews_counter(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(count=Count('pk'))
        counter = 0
        if reviews["count"] is not None:
            counter = int(reviews["count"])
        return counter

    def reviews_avg_hop(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('hop'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg

    def reviews_avg_malt(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('malt'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg

    def reviews_avg_roast(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('roast'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg

    def reviews_avg_smoke(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('smoke'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg

    def reviews_avg_fruit(self):
        content_type = ContentType.objects.get_for_model(self)
        reviews = Review.objects.filter(
            content_type=content_type,
            object_pk=self.pk
        ).aggregate(average=Avg('fruit'))
        avg = 0
        if reviews["average"] is not None:
            # round - rounding the number up to 1 decimal place
            avg = round(float(reviews["average"]), 1)
        return avg


class Beer(BeerMain):
    brewery = models.CharField(max_length=25)
    # Only Beers approved by admin should be shown in the Beer Ranking page - default False
    isapproved = models.BooleanField(default=False)

    # Function that set isapproved to True - Beer is shown in the Beer Ranking
    def approve(self):
        self.isapproved = True
        self.save()

    def __str__(self):
        return self.name


class MyBeer(BeerMain):
    description = models.CharField(max_length=250, null=True, blank=True)
    malts = models.CharField(max_length=250, null=True, blank=True)
    hops = models.CharField(max_length=250, null=True, blank=True)
    additives = models.CharField(max_length=250, null=True, blank=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(MyBeer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    product = models.TextField(max_length=250)
    price = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending')
