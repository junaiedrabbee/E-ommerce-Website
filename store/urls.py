from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact_us, name='contact_us'),
    path('blogs/', views.blogs, name='blogs'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
       path('register/', views.register, name='register'),
        path('create-profile/', views.create_profile, name='create_profile'),
           path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

]
