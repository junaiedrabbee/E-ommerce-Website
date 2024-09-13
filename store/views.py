from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from .models import Blog, Product, Customer, Order, OrderItem, ContactMessage
from .forms import ContactForm
from .models import UserProfile
from .forms import UserProfileForm
from .forms import RegisterForm
from .forms import ProfileForm 

def home(request):
    blogs = Blog.objects.all()[:4]
    most_sold_products = Product.objects.order_by('-sales')[:5]
    discount_products = Product.objects.filter(discount__gt=0)[:6]
    new_products = Product.objects.order_by('-id')[:4]
    context = {
        'blogs': blogs,
        'most_sold_products': most_sold_products,
        'discount_products': discount_products,
        'new_products': new_products,
    }
    return render(request, 'store/index.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

@login_required(login_url='login')
def cart(request):
    try:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # Fetch all OrderItems related to the order
        cart_total = order.get_cart_total
        cart_items = order.get_cart_items
    except Customer.DoesNotExist:
        # Handle case when customer does not exist
        items = []
        cart_total = 0
        cart_items = 0

    context = {
        'items': items,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)




@login_required(login_url='login')
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)

# store/models.py

from django.db import models
from django.contrib.auth.models import User




def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            
            # Add a success message
            messages.success(request, 'Your message has been sent successfully!')
            
            return redirect('contact_success')  # Correct the URL name, no dot at the end
    else:
        form = ContactForm()
    
    return render(request, 'store/contact_us.html', {'form': form})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def blogs(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'store/blog_details.html', context)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'store/blog_detail.html'
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer  # Ensure this customer exists
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1  # Increment the quantity if the item already exists
    order_item.save()
    
    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('store')




@login_required(login_url='login')
def update_cart(request, item_id, action):
    order = get_object_or_404(Order, customer=request.user.customer, complete=False)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
    item.save()
    return redirect('cart')
def contact_success(request):
    return render(request, 'store/contact_success.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a customer object for the user
            Customer.objects.create(user=user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Redirect to a page where users can create their profile or display a message
        return redirect('create_profile')  # or a message or some other handling
    
    return render(request, 'store/profile.html', {'profile': user_profile})
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')  # Redirect to the profile page
    else:
        form = UserProfileForm()
    return render(request, 'store/profile.html', {'form': form})

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page or another page
    else:
        form = ProfileForm(instance=user_profile)
    
    return render(request, 'store/update_profile.html', {'form': form})
# store/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer


