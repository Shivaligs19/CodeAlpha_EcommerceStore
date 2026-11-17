from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem


# Homepage
def home(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Product.objects.order_by('category').values_list(
        'category',
        flat=True
    ).distinct()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
    })


# Product Details Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {
        'product': product
    })


# Add to Cart
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:
            messages.error(request, 'Product is out of stock.')
            return redirect('home')

        cart = request.session.get('cart', {})
        product_id = str(product_id)

        current_quantity = cart.get(product_id, 0)

        if current_quantity < product.stock:
            cart[product_id] = current_quantity + 1
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Product added to cart!')
        else:
            messages.error(request, 'Maximum available stock reached.')

    return redirect('cart')


# Update Cart
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        if product_id in cart:
            try:
                quantity = int(request.POST.get('quantity', 1))
                product = get_object_or_404(Product, id=product_id)

                if quantity < 1:
                    del cart[product_id]
                elif quantity <= product.stock:
                    cart[product_id] = quantity
                else:
                    messages.error(request, 'Requested quantity is unavailable.')

                request.session['cart'] = cart
                request.session.modified = True

            except ValueError:
                messages.error(request, 'Invalid quantity.')

    return redirect('cart')


# Cart Page
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            subtotal = product.price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

            total += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# Remove from Cart
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Product removed from cart.')

    return redirect('cart')


# User Registration
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')

    return render(request, 'register.html')


# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# Checkout
def checkout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login before checkout.')
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not full_name or not address or not phone:
            messages.error(request, 'Please fill in all delivery details.')

        else:
            with transaction.atomic():
                valid_stock = True

                for item in cart_items:
                    product = Product.objects.select_for_update().get(
                        id=item['product'].id
                    )

                    if product.stock < item['quantity']:
                        valid_stock = False
                        break

                if not valid_stock:
                    messages.error(
                        request,
                        'Some products have insufficient stock. Please update your cart.'
                    )

                else:
                    order = Order.objects.create(
                        user=request.user,
                        full_name=full_name,
                        address=address,
                        phone=phone,
                        total_amount=total
                    )

                    for item in cart_items:
                        product = Product.objects.select_for_update().get(
                            id=item['product'].id
                        )

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item['quantity'],
                            price=product.price
                        )

                        product.stock -= item['quantity']
                        product.save()

                    request.session['cart'] = {}
                    request.session.modified = True

                    return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


# Order Success Page
def order_success(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, 'order_success.html', {
        'order': order
    })
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request, 'order_history.html', {
        'orders': orders
    })