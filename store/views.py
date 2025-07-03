from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Category  # pas aan op basis van je model
from django.views.decorators.http import require_POST
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'store/cart.html')

    line_items = []
    order = Order.objects.create(user=request.user if request.user.is_authenticated else None)

    for product_id, item in cart.items():
        product = Product.objects.get(pk=product_id)
        # Haal quantity uit item, of item zelf als int
        if isinstance(item, dict):
            quantity = int(item.get('quantity', 1))
        else:
            quantity = int(item)

        line_items.append({
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(float(product.price) * 100),
                'product_data': {'name': product.name},
            },
            'quantity': quantity,
        })

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url, code=303)


def success(request):
    session_id = request.GET.get('session_id')
    print("Ontvangen session_id:", session_id)
    if not session_id:
        return redirect('product_list')

    try:
        order = Order.objects.get(stripe_session_id=session_id)
        order.paid = True
        order.save()
        request.session['cart'] = {}  # Leeg het winkelmandje
    except Order.DoesNotExist:
        print("Order met deze session_id bestaat niet!")

    return render(request, 'store/success.html')


def cancel(request):
    return render(request, 'store/cancel.html')


def home_view(request):
    recent_orders = []
    categories = Category.objects.all()
    if request.user.is_authenticated:
        recent_orders = Order.objects.filter(user=request.user, paid=True).order_by('-created_at')[:5]
    return render(request, 'store/home.html', {'recent_orders': recent_orders, 'categories':categories})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)

    product_key = str(product_id)

    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url,
        }

    request.session['cart'] = cart

    return redirect('product_list')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, pk=product_id)

        # Als item een int is, interpreteer het als oude stijl: alleen quantity
        if isinstance(item, int):
            quantity = item
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
                'image': product.image.url  # fallback naar huidige image
            })
        elif isinstance(item, dict):
            quantity = item.get('quantity', 1)
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
                'image': item.get('image', product.image.url)
            })
        else:
            continue  # Onverwacht type? Sla over.

        total_price += item_total

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@require_POST
def update_cart_quantity(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    product_key = str(product_id)

    if product_key in cart:
        cart_item = cart[product_key]
        if isinstance(cart_item, dict):
            cart_item['quantity'] = quantity
        else:
            cart[product_key] = {
                'quantity': quantity
            }

        request.session['cart'] = cart
    return redirect('view_cart')
# Create your views here.


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, paid=True).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})
