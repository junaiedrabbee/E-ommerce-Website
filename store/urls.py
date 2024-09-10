from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('blogs/', views.blogs, name='blogs'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
