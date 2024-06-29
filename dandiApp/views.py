from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, About, Order, Suggestion, Cart, CartItem
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, redirect



def home(request):
    return render(request, 'home.html')
def product_list(request):
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'categories': categories})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products_by_category.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')
        total_price = product.price * quantity

        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            payment_status=False
        )

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'order_product.html', {'product': product})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def about(request):
    about_infos = About.objects.all()
    return render(request, 'about.html', {'about_infos': about_infos})

def submit_suggestion(request):
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['message']
        Suggestion.objects.create(email=email, message=message)
        return redirect('home')
    return HttpResponse(status=405)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    previous_orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'previous_orders': previous_orders})

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=User.objects.get(email=email).username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')

        for item in cart_items:
            Order.objects.create(
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price(),
                customer_name=request.user.username,  # Utiliser le nom d'utilisateur connecté
                customer_phone=customer_phone,
                customer_address=customer_address,
                payment_status=False,
                user=request.user  # Associer à l'utilisateur connecté
            )
        cart.items.all().delete()  # Vider le panier après validation
        return redirect('order_confirmation_authenticated')

    return render(request, 'checkout_authenticated.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def order_confirmation_authenticated(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'order_confirmation_authenticated.html', {'orders': orders})


