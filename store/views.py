from django.shortcuts import render, get_object_or_404
from .models import Blog, Product, Customer, Order, OrderItem  # Ensure correct imports
from django.views.generic import DetailView

def home(request):
    blogs = Blog.objects.all()[:4]
    most_sold_products = Product.objects.order_by('-sales')[:6]
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
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_total = order.get_cart_total
        cart_items = order.get_cart_items
    else:
        items = []
        cart_total = 0
        cart_items = 0

    context = {
        'items': items,
        'order': order,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)

def profile(request):
    return render(request, 'store/profile.html')

def contact(request):
    return render(request, 'store/contact.html')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def blogs(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'store/blog_details.html', context)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'store/blog_detail.html'
