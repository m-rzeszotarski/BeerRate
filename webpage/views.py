from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Beer, Review
from .forms import BeerForm, ReviewForm, NewUserForm
from django.contrib import messages


def home(request):
    return render(request, 'webpage/home.html', {})


def beer_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/beer_list.html', {'beers': beers})


def beer_detail(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    review = Review.objects.filter(beer=beer)
    # Only not banned reviews are considered
    reviews = beer.reviews.filter(banned=False)

    new_review = None

    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # Create Review object but don't save to database yet
            new_review = review_form.save(commit=False)
            # Assign the current beer to the review
            new_review.beer = beer
            # Assign logged username to 'author' field
            new_review.author = request.user
            # Save the review to the database
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request, 'webpage/beer_detail.html', {'beer': beer,
                                                        'review': review,
                                                        'reviews': reviews,
                                                        'new_review': new_review,
                                                        'review_form': review_form})


@login_required
def beer_new(request):
    if request.method == "POST":
        form = BeerForm(request.POST)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.author = request.user
            beer.published_date = timezone.now()
            beer.save()
            return redirect('beer_detail', pk=beer.pk)
    else:
        form = BeerForm()
    return render(request, 'webpage/beer_edit.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def beer_edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.author = request.user
            beer.published_date = timezone.now()
            beer.save()
            return redirect('beer_detail', pk=beer.pk)
    else:
        form = BeerForm(instance=beer)
    return render(request, 'webpage/beer_edit.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def beer_remove(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.delete()
    return redirect('beer_list')


@user_passes_test(lambda u: u.is_superuser)
def beer_approve(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.approve()
    return redirect('beer_list')


@user_passes_test(lambda u: u.is_superuser)
def approve_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/approve_list.html', {'beers': beers})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
    return render(request, "registration/register.html", {"register_form": form})

