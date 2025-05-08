from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, StoreForm, ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import vendor_required, buyer_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Store, Product, Profile, Review, Purchase
from django.views.decorators.http import require_POST
from .forms import ReviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from django.db import transaction


def register_view(request): 
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            user.set_password(raw_password)
            user.save()

            # Create the profile and assign role
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, role=role)

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            # Ensure the user has a profile
            profile, created = Profile.objects.get_or_create(user=user)

            login(request, user)
            role = profile.role
            if role == 'vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('buyer_dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and profile.role == 'vendor':
            return redirect('vendor_dashboard')
        else:
            return render(request, 'shop/home.html')  
    return render(request, 'shop/home.html')

@login_required
def buyer_dashboard(request):
    stores = Store.objects.all()
    return render(request, 'shop/buyer_dashboard.html', {'stores': stores})


def is_vendor(user):
    return hasattr(user, 'profile') and user.profile.role == 'vendor'

@login_required
@vendor_required
def vendor_dashboard(request):
    if not is_vendor(request.user):
        return redirect('home')
    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'shop/vendor_dashboard.html', {'stores': stores})

@login_required
def create_store(request):
    if not is_vendor(request.user):
        return redirect('home')

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.owner = request.user  # Set owner too!
            store.save()
            messages.success(request, "Store created successfully.")
            return redirect('vendor_dashboard')
        else:
            print(form.errors)  # Log form errors for debugging
    else:
        form = StoreForm()

    return render(request, 'shop/create_store.html', {'form': form})



@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated.")
            return redirect('vendor_dashboard')
    else:
        form = StoreForm(instance=store)
    return render(request, 'shop/edit_store.html', {'form': form})

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    store.delete()
    messages.success(request, "Store deleted.")
    return redirect('vendor_dashboard')

@login_required
def manage_products(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)
    return render(request, 'shop/manage_products.html', {'store': store, 'products': products})

@login_required
def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, "Product added.")
            return redirect('manage_products', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'shop/add_products.html', {'form': form, 'store': store})

@login_required
def vendor_products(request):
    stores = Store.objects.filter(owner=request.user)
    products = Product.objects.filter(store__in=stores)
    return render(request, 'shop/vendor_products.html', {'products': products})

@login_required
def edit_product(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id)
    product = get_object_or_404(Product, id=product_id, store=store)

    # Only allow owner or vendor to edit
    if request.user != store.owner and request.user != store.vendor:
        return redirect('product_list', store_id=store_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', store_id=store_id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_edit.html', {'form': form, 'store': store, 'product': product})


@require_POST
@login_required
def delete_product(request, store_id, product_id):
    product = get_object_or_404(Product, id=product_id, store_id=store_id)
    store = get_object_or_404(Store, id=store_id)

    if request.user == store.owner or request.user == store.vendor:
        product.delete()

    return redirect('product_list', store_id=store_id)

@login_required
def product_list(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)
    return render(request, 'shop/product_list.html', {'store': store, 'products': products})

@login_required
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'shop/store_list.html', {'stores': stores})

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'shop/store_detail.html', {'store': store, 'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    
    # Removed profile reference, using request.user directly for Purchase query
    has_purchased = Purchase.objects.filter(buyer=request.user, product=product).exists()
    
    if request.method == 'POST':
        #content = request.POST.get('content')
        comment = request.POST.get('comment')

        rating = int(request.POST.get('rating', 0))
        
        if comment and rating:
            # is_verified depends on whether the user has purchased the product
            is_verified = has_purchased
            Review.objects.create(
                user=request.user,
                product=product,
                comment=comment,
                rating=rating,
                is_verified=is_verified
            )
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, "Please provide both content and a rating for your review.")
            return redirect('product_detail', product_id=product_id)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'has_purchased': has_purchased
    })

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    buyer = request.user

    # Check if user has purchased this product before
    has_purchased = Purchase.objects.filter(buyer=request.user, product=product).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.buyer = buyer
            review.verified = has_purchased
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'shop/submit_review.html', {'form': form, 'product': product})

from decimal import Decimal  # just in case you use Decimal elsewhere

def add_to_cart(request, product_id):
    from django.contrib import messages
    from django.shortcuts import redirect, get_object_or_404
    from .models import Product

    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'quantity': 1,
            'price': float(product.price)  # Convert Decimal to float here
        }

    request.session['cart'] = cart
    messages.success(request, f"'{product.name}' added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


from decimal import Decimal

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            price = Decimal(str(item['price']))  # Convert float from session to Decimal
            subtotal = price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)

        request.session['cart'] = cart
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')



@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('view_cart')

    cart_items = []
    total_price = 0

    try:
        with transaction.atomic():  # Ensure atomicity to prevent race conditions
            for product_id, item in cart.items():
                try:
                    product = Product.objects.select_for_update().get(pk=product_id)
                    quantity = item.get('quantity', 1)

                    if product.stock < quantity:
                        messages.warning(request, f"Not enough stock for {product.name}. Skipping.")
                        continue

                    # Create purchase records
                    for _ in range(quantity):
                        Purchase.objects.create(buyer=request.user, product=product)

                    # Deduct stock
                    product.stock -= quantity
                    product.save()

                    # Add to invoice
                    subtotal = product.price * quantity
                    total_price += subtotal
                    cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

                except Product.DoesNotExist:
                    continue

    except Exception as e:
        messages.error(request, "Something went wrong during checkout.")
        return redirect('view_cart')

    if not cart_items:
        messages.warning(request, "No items were purchased due to stock issues.")
        return redirect('view_cart')

    # Prepare and send the invoice email
    subject = 'Your Purchase Receipt'
    message = render_to_string('shop/email_invoice.html', {
        'user': request.user,
        'cart_items': cart_items,
        'total_price': total_price,
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )

    # Clear the cart
    request.session['cart'] = {}

    return redirect('order_confirmation')

def order_confirmation(request):
    return render(request, 'shop/order_confirmation.html')
