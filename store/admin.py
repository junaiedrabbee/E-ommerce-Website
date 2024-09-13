from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress, Blog, ContactMessage
from django import forms
from .models import UserProfile
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Blog)
admin.site.register(ContactMessage)
# store/admin.py


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ('user', 'bio', 'profile_picture')

admin.site.register(UserProfile, UserProfileAdmin)
