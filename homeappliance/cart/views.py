from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product, OrderItem, Order
from .models import Cart, CartItem
from django.contrib import messages


# ===== Session Cart Helpers =====

def get_session_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def save_session_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def merge_session_cart_to_db(request):
    session_cart = get_session_cart(request)
    if not session_cart:
        return

    db_cart, _ = Cart.objects.get_or_create(customer=request.user.customer)

    for product_id, quantity in session_cart.items():
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            continue
        item, created = CartItem.objects.get_or_create(cart=db_cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

    request.session['cart'] = {}
    request.session.modified = True


# ===== Cart Helpers =====

def get_cart_data(request):
    if request.user.is_authenticated:
        try:
            db_cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
            items = db_cart.items.all().select_related('product')
            total = db_cart.get_total()
            count = db_cart.get_count()
        except Exception:
            items, total, count = [], 0, 0
    else:
        session_cart = get_session_cart(request)
        items = []
        total = 0
        count = 0
        for product_id, quantity in session_cart.items():
            product = Product.objects.filter(pk=product_id).first()
            if product:
                price = product.on_sale_price if product.on_sale else product.price
                subtotal = price * quantity
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal,
                    'id': product_id,
                })
                total += subtotal
                count += quantity

    return items, total, count

# ===== Views =====

def cart_detail(request):
    items, total, count = get_cart_data(request)
    return render(request, 'cart.html', {
        'items': items,
        'total': total,
        'count': count,
        'is_authenticated': request.user.is_authenticated,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        db_cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
        item, created = CartItem.objects.get_or_create(cart=db_cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
    else:
        session_cart = get_session_cart(request)
        pid = str(product_id)
        session_cart[pid] = session_cart.get(pid, 0) + 1
        save_session_cart(request, session_cart)

    return redirect(request.META.get('HTTP_REFERER', 'shop_main_page'))


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, pk=item_id, cart__customer=request.user.customer)
        item.delete()
    else:
        session_cart = get_session_cart(request)
        pid = str(item_id)
        if pid in session_cart:
            del session_cart[pid]
            save_session_cart(request, session_cart)

    return redirect('cart_detail')


def update_cart(request, item_id):
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, pk=item_id, cart__customer=request.user.customer)
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    else:
        session_cart = get_session_cart(request)
        pid = str(item_id)
        if quantity > 0:
            session_cart[pid] = quantity
        else:
            session_cart.pop(pid, None)
        save_session_cart(request, session_cart)

    return redirect('cart_detail')

@login_required
def checkout(request):
    items, total, count = get_cart_data(request)

    if not items:
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart_detail')

    customer = request.user.customer

    if request.method == 'POST':
        province = request.POST.get('province', '').strip()
        city = request.POST.get('city', '').strip()
        address = request.POST.get('address', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not province or not city or not address or not phone:
            messages.error(request, 'لطفاً اطلاعات ضروری سفارش را کامل وارد کنید.')
            return redirect('checkout')

        order = Order.objects.create(
            customer=customer,
            province=province,
            city=city,
            address=address,
            postal_code=postal_code,
            phone=phone,
        )

        for item in items:
            product = item.product
            price = product.on_sale_price if product.on_sale else product.price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=price,
            )

        cart = Cart.objects.filter(customer=customer).first()
        if cart:
            cart.items.all().delete()

        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return redirect('profile')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
        'count': count,
        'customer': customer,
    })