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


# @login_required - decorator allowing only logged-in users to use it
# @user_passes_test - decorator allowing superuser only to use it
# @csrf_exempt used to avoid Django expecting a CSRF token (used for paypal integration purpose)


# Home page
def home(request):
    return render(request, 'webpage/home.html', {})


# View for new user registration
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


# View showing all beers
def beer_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/beer_list.html', {'beers': beers})


# This is a view for displaying a details of beers and mybeers (beer_detail.html and mybeer_detail.html)
# request, model - Beer or MyBeer, template_name - 'webpage/beer_detail.html' or 'webpage/mybeer_detail.html', pk
def detail(request, model, template_name, pk):
    # get beer or mybeer
    product = get_object_or_404(model, pk=pk)

    # chart_labels and chart_data are used by Chart.js
    chart_labels = ['Hop', 'Malt', 'Roast', 'Smoke', 'Fruit']

    # average from users rating
    chart_data = [product.reviews_avg('hop'),
                  product.reviews_avg('malt'),
                  product.reviews_avg('roast'),
                  product.reviews_avg('smoke'),
                  product.reviews_avg('fruit')]

    # It is necessary to get ContentType because Review use GenericForeignKey
    content_type = ContentType.objects.get_for_model(product)
    # Filter reviews to get reviews of selected beer
    reviews = Review.objects.filter(content_type=content_type, object_pk=product.pk)

    new_review = None

    # creating new review
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # filtering reviews for selected beer and logged user
            old_review = reviews.filter(author=request.user)
            # counting number of reviews for selected beer created by logged user
            # if number of review is greater than 0 script deletes old review
            if old_review.count() > 0:
                old_review.delete()
            # Create Review object but don't save to database yet
            new_review = review_form.save(commit=False)
            # Assign the current content_type (beer) and pk to the review
            new_review.content_type = content_type
            new_review.object_pk = product.pk
            # Assign logged username to 'author' field
            new_review.author = request.user
            # Save the review to the database
            new_review.save()
    else:
        review_form = ReviewForm()

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'reviews': reviews,
        'new_review': new_review,
        'review_form': review_form,
    }

    # Render depends on model type
    if model == Beer:
        context['beer'] = product
    elif model == MyBeer:
        context['mybeer'] = product

    return render(request, template_name, context)


def beer_detail(request, pk):
    return detail(request, Beer, 'webpage/beer_detail.html', pk)


def mybeer_detail(request, pk):
    return detail(request, MyBeer, 'webpage/mybeer_detail.html', pk)


# view for creating a new beer
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
            # updates author field
            beer.author = str(request.user)
            beer.published_date = timezone.now()
            beer.save()
            return redirect('beer_detail', pk=beer.pk)
    else:
        form = BeerForm(instance=beer)
    return render(request, 'webpage/beer_edit.html', {'form': form})


# view for handling removing beers and mybeers
@user_passes_test(lambda u: u.is_superuser)
def object_remove(request, model, template_name, pk):
    product = get_object_or_404(model, pk=pk)
    # Deletes all reviews for beers and mybeers
    if model == Beer or model == MyBeer:
        product.reviews.all().delete()
    product.delete()
    return redirect(template_name)


# view for removing beer
@user_passes_test(lambda u: u.is_superuser)
def beer_remove(request, pk):
    return object_remove(request, Beer, 'beer_list', pk)


# view for removing mybeer
@user_passes_test(lambda u: u.is_superuser)
def mybeer_remove(request, pk):
    return object_remove(request, MyBeer, 'mybeer_list', pk)


# view for removing chosen products from cart
@login_required
def remove_from_cart(request, pk):
    return object_remove(request, CartItem, 'view_cart', pk)


# View for removing orders
@user_passes_test(lambda u: u.is_superuser)
def order_remove(request, pk):
    return object_remove(request, Order, 'order_list', pk)


# beer have to be approved by superuser before it will be shown in beer_list.html page
@user_passes_test(lambda u: u.is_superuser)
def beer_approve(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    # Uses function built-in class
    beer.approve()
    return redirect('beer_list')


# view listing beers (used in approve_list.html)
@user_passes_test(lambda u: u.is_superuser)
def approve_list(request):
    beers = Beer.objects.all()
    return render(request, 'webpage/approve_list.html', {'beers': beers})


# view listing mybeers (ecommerce)
def mybeer_list(request):
    mybeers = MyBeer.objects.all()
    return render(request, 'webpage/mybeer_list.html', {'mybeers': mybeers})


# view for editing mybeers (ecommerce)
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


# view for creating my beers (ecommerce)
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


# view showing items in cart (ecommerce)
@login_required
def view_cart(request):
    # Cart is showing products added by logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    # Calculating total price of products in cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'webpage/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# view for adding mybeers into the cart (mybeer -> cart_item) (ecommerce)
@login_required
def add_to_cart(request, pk):
    product = MyBeer.objects.get(pk=pk)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)

    cart_item.quantity += 1
    cart_item.save()
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


# view for making a new order in shop
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


# View for payment page (django-paypal integration)
def payment_process(request):
    order_pk = request.session.get('order_pk')
    order = get_object_or_404(Order, pk=order_pk)
    host = request.get_host()

    paypal_dict = {
        # My paypal email (from settings.py)
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        # Price that paypal will charge
        "amount": str(order.price),
        # Ordered products
        "item_name": str(Order.product),
        # Invoice number - for now I left the order number
        "invoice": str(order.pk),
        # Currency for paypal
        "currency_code": 'PLN',
        # Redirect user to paypal payment if successful -> payment_done.html if not payment_canceled.html
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "webpage/payment_process.html", {'order': order,
                                                            'form': form})


# View for completed payment
@csrf_exempt
def payment_done(request):
    return render(request, 'webpage/payment_done.html')


# View for not completed payment
@csrf_exempt
def payment_canceled(request):
    return render(request, 'webpage/payment_canceled.html')


# View for editing the order
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


# View showing all orders in database
@user_passes_test(lambda u: u.is_superuser)
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'webpage/order_list.html', {'orders': orders})


# View for changing order status
@user_passes_test(lambda u: u.is_superuser)
def order_status_change(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    order.status = status
    order.save()
    return redirect('order_list')


# view showing the orders assigned to logged-in user
def order_status(request):
    orders = Order.objects.filter(author=request.user)
    return render(request, 'webpage/order_status.html', {'orders': orders})


# View for handling banning or unbanning reviews
# Because of usage of GenericForeignKey content_type must be differentiated (beer or mybeer)
# Also depending on content_type user is redirected to different pages
@user_passes_test(lambda u: u.is_superuser)
def handle_review_ban(request, review, is_banned):
    review.banned = is_banned
    review.save()

    if review.content_type == ContentType.objects.get_for_model(Beer):
        return redirect('beer_detail', pk=review.object_pk)
    elif review.content_type == ContentType.objects.get_for_model(MyBeer):
        return redirect('mybeer_detail', pk=review.object_pk)


# View for banning reviews
@user_passes_test(lambda u: u.is_superuser)
def review_ban(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return handle_review_ban(request, review, is_banned=True)


# View for unbanning reviews
@user_passes_test(lambda u: u.is_superuser)
def review_unban(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return handle_review_ban(request, review, is_banned=False)
