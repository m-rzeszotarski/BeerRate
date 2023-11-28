from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Beer
from .forms import BeerForm
def home(request):
    return render(request, 'webpage/home.html', {})

def beer_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/beer_list.html', {'beers' : beers})


def beer_detail(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    rating = Rating.objects.filter(beer=beer, user=request.user).first()
    beer.user_rating = rating.rating if rating else 0
    return render(request, 'webpage/beer_detail.html', {'beer' : beer})

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
@login_required
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

@login_required
def beer_remove(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.delete()
    return redirect('beer_list')

@login_required
def beer_approve(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.approve()
    return redirect('beer_list')

@login_required
def approve_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/approve_list.html', {'beers' : beers})