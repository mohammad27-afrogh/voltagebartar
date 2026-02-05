from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'national_number',
            'province_address',
            'city_address',
            'exact_address',
            'postal_code',
            'email',
            'order_notes',
        ]
