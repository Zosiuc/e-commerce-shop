from django.shortcuts import render, redirect, get_object_or_404
from .models import Product  # pas aan op basis van je model
from django.views.decorators.http import require_POST


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
    return redirect('view_cart')


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
