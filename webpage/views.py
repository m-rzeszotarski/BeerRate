from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .models import Beer, Review, MyBeer, CartItem, Order
from .forms import BeerForm, ReviewForm, NewUserForm, MyBeerForm, OrderForm
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.contenttypes.models import ContentType


def home(request):
    return render(request, 'webpage/home.html', {})


# view for new user registration
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


# view showing all beers
def beer_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/beer_list.html', {'beers': beers})


# view showing details of chosen beer
def beer_detail(request, pk):
    beer = get_object_or_404(Beer, pk=pk)

    chart_labels = ['Hop', 'Malt', 'Roast', 'Smoke', 'Fruit']
    chart_data = [beer.reviews_avg_hop(),
                  beer.reviews_avg_malt(),
                  beer.reviews_avg_roast(),
                  beer.reviews_avg_smoke(),
                  beer.reviews_avg_fruit()]

    content_type = ContentType.objects.get_for_model(beer)

    reviews = Review.objects.filter(content_type=content_type, object_pk=beer.pk)
    # Only not banned reviews are considered

    new_review = None

    # creating new review
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            content_type = ContentType.objects.get_for_model(beer)
            # filtering reviews for selected beer and logged user
            old_review = Review.objects.filter(content_type=content_type, object_pk=beer.pk, author=request.user)
            # counting number of review for selected beer created by logged user
            old_review_count = old_review.count()
            # if number of review is greater than 0 script deletes old review
            # (only one review can be created by one user)
            if old_review_count > 0:
                old_review.delete()
            # Create Review object but don't save to database yet
            new_review = review_form.save(commit=False)
            # Assign the current beer to the review
            new_review.content_type = content_type
            new_review.object_pk = beer.pk
            # Assign logged username to 'author' field
            new_review.author = request.user
            # Save the review to the database
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request, 'webpage/beer_detail.html', {'beer': beer,
                                                        'chart_labels': chart_labels,
                                                        'chart_data': chart_data,
                                                        'reviews': reviews,
                                                        'new_review': new_review,
                                                        'review_form': review_form})


# view for new beer - @login_required - decorator allowing only logged-in users to use it
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


# view for editing existing beer
@login_required
def beer_edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.author = str(request.user)
            beer.published_date = timezone.now()
            beer.save()
            return redirect('beer_detail', pk=beer.pk)
    else:
        form = BeerForm(instance=beer)
    return render(request, 'webpage/beer_edit.html', {'form': form})


# view for removing beer - @user_passes_test - decorator allowing superuser only to use it
@user_passes_test(lambda u: u.is_superuser)
def beer_remove(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.reviews.all().delete()
    beer.delete()
    return redirect('beer_list')


# beer have to be approved by superuser before it will be shown in beer_list page
@user_passes_test(lambda u: u.is_superuser)
def beer_approve(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.approve()
    return redirect('beer_list')


# view listing beers in approve_list.html
@user_passes_test(lambda u: u.is_superuser)
def approve_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/approve_list.html', {'beers': beers})


# view listing mybeers (shop)
def mybeer_list(request):
    mybeers = MyBeer.objects.all()
    return render(request, 'webpage/mybeer_list.html', {'mybeers': mybeers})


# view for editing mybeers (shop)
@user_passes_test(lambda u: u.is_superuser)
def mybeer_edit(request, pk):
    mybeer = get_object_or_404(MyBeer, pk=pk)
    if request.method == "POST":
        form = MyBeerForm(request.POST, instance=mybeer)
        if form.is_valid():
            mybeer = form.save(commit=False)
            mybeer.author = str(request.user)
            mybeer.published_date = timezone.now()
            mybeer.save()
            return redirect('mybeer_detail', pk=mybeer.pk)
    else:
        form = MyBeerForm(instance=mybeer)
    return render(request, 'webpage/mybeer_edit.html', {'form': form})


# view for removing mybeers (shop)
@user_passes_test(lambda u: u.is_superuser)
def mybeer_remove(request, pk):
    mybeer = get_object_or_404(MyBeer, pk=pk)
    mybeer.reviews.all().delete()
    mybeer.delete()
    return redirect('mybeer_list')


# view for creating my beers (shop)
@user_passes_test(lambda u: u.is_superuser)
def mybeer_new(request):
    if request.method == "POST":
        form = MyBeerForm(request.POST)
        if form.is_valid():
            mybeer = form.save(commit=False)
            mybeer.author = request.user
            mybeer.published_date = timezone.now()
            mybeer.save()
            return redirect('mybeer_detail', pk=mybeer.pk)
    else:
        form = MyBeerForm()
    return render(request, 'webpage/mybeer_edit.html', {'form': form})


# view showing details of chosen my beer (shop)
def mybeer_detail(request, pk):
    mybeer = get_object_or_404(MyBeer, pk=pk)

    chart_labels = ['Hop', 'Malt', 'Roast', 'Smoke', 'Fruit']
    chart_data = [mybeer.reviews_avg_hop(),
                  mybeer.reviews_avg_malt(),
                  mybeer.reviews_avg_roast(),
                  mybeer.reviews_avg_smoke(),
                  mybeer.reviews_avg_fruit()]

    content_type = ContentType.objects.get_for_model(mybeer)

    reviews = Review.objects.filter(content_type=content_type, object_pk=mybeer.pk)
    # Only not banned reviews are considered

    new_review = None

    # creating new review
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            content_type = ContentType.objects.get_for_model(mybeer)
            # filtering reviews for selected beer and logged user
            old_review = Review.objects.filter(content_type=content_type, object_pk=mybeer.pk, author=request.user)
            # counting number of review for selected beer created by logged user
            old_review_count = old_review.count()
            # if number of review is greater than 0 script deletes old review
            # (only one review can be created by one user)
            if old_review_count > 0:
                old_review.delete()
            # Create Review object but don't save to database yet
            new_review = review_form.save(commit=False)
            # Assign the current beer to the review
            new_review.content_type = content_type
            new_review.object_pk = mybeer.pk
            # Assign logged username to 'author' field
            new_review.author = request.user
            # Save the review to the database
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request, 'webpage/mybeer_detail.html', {'mybeer': mybeer,
                                                          'chart_labels': chart_labels,
                                                          'chart_data': chart_data,
                                                          'reviews': reviews,
                                                          'new_review': new_review,
                                                          'review_form': review_form})


# view showing items in cart (shop)
@login_required
def view_cart(request):
    # Cart is showing products added by logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    # Calculating total price of products in cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'webpage/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# view for adding products into the cart (shop)
@login_required
def add_to_cart(request, pk):
    product = MyBeer.objects.get(pk=pk)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)

    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


# view for removing chosen products from cart
@login_required
def remove_from_cart(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect('view_cart')


# view for increasing amount of selected product in cart
@login_required
def increase_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


# view for decreasing amount of selected product in cart
@login_required
def decrease_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')


# view for making new order in shop
@login_required
def make_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.date = timezone.now()
            # cart_items created to help calculate order.price
            cart_items = CartItem.objects.filter(user=request.user)
            order.price = sum(item.product.price * item.quantity for item in cart_items)
            # Add shipping charge
            if order.shipping == 'dpd':
                order.price += 25
            elif order.shipping == 'inpost':
                order.price += 15
            elif order.shipping == 'poczta':
                order.price += 35
            # Products (Query Set) in cart converted into the string
            order.product = str(CartItem.objects.filter(user=request.user))
            # Stripping string from Query Set specific elements
            order.product = order.product.replace('<QuerySet [', '')
            order.product = order.product.replace('>]>', '')
            order.product = order.product.replace('<CartItem:', '')
            order.product = order.product.replace('>', '')
            order.save()
            # Order saved - products should be removed from cart
            CartItem.objects.filter(user=request.user).delete()
            request.session['order_pk'] = order.pk
            return redirect(reverse('payment_process'))
    else:
        form = OrderForm()
    return render(request, 'webpage/order_edit.html', {'form': form})


def payment_process(request):
    order_pk = request.session.get('order_pk')
    order = get_object_or_404(Order, pk=order_pk)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(order.price),
        "item_name": str(Order.product),
        "invoice": str(order.pk),
        "currency_code": 'PLN',
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_canceled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "webpage/payment_process.html", {'order': order,
                                                            'form': form})


# view showing the order detail - @csrf_exempt used to avoid Django expecting a CSRF token
# since PayPal can redirect the user to this view by POST
@csrf_exempt
def payment_done(request):
    return render(request, 'webpage/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'webpage/payment_canceled.html')


# view for editing the order

def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = str(request.user)
            order.date = timezone.now()
            order.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'webpage/order_edit.html', {'form': form})


# view showing all orders in database (superuser only)
@user_passes_test(lambda u: u.is_superuser)
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'webpage/order_list.html', {'orders': orders})


# view for removing orders
@user_passes_test(lambda u: u.is_superuser)
def order_remove(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')


# view for changing order status to 'pending'
@user_passes_test(lambda u: u.is_superuser)
def order_pending(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Pending'
    order.save()
    return redirect('order_list')


# view for changing order status to 'shipped'
@user_passes_test(lambda u: u.is_superuser)
def order_shipped(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Shipped'
    order.save()
    return redirect('order_list')


# view for changing order status to 'cancelled' (user also can cancel the order)
@login_required
def order_cancelled(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_list')


# view for changing order status to 'completed'
@user_passes_test(lambda u: u.is_superuser)
def order_completed(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Completed'
    order.save()
    return redirect('order_list')


# view for changing order status to 'delayed'
@user_passes_test(lambda u: u.is_superuser)
def order_delayed(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Delayed'
    order.save()
    return redirect('order_list')


# view showing the orders assigned to logged-in user
def order_status(request):
    orders = Order.objects.filter(author=request.user)
    return render(request, 'webpage/order_status.html', {'orders': orders})


@user_passes_test(lambda u: u.is_superuser)
def handle_review_ban(request, review, is_banned):
    review.banned = is_banned
    review.save()

    if review.content_type == ContentType.objects.get_for_model(Beer):
        return redirect('beer_detail', pk=review.object_pk)
    elif review.content_type == ContentType.objects.get_for_model(MyBeer):
        return redirect('mybeer_detail', pk=review.object_pk)


@user_passes_test(lambda u: u.is_superuser)
def review_ban(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return handle_review_ban(request, review, is_banned=True)


@user_passes_test(lambda u: u.is_superuser)
def review_unban(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return handle_review_ban(request, review, is_banned=False)
