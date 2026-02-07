from django import forms
from .models import Order, Profile


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'national_number',
            'email',
            'province_address',
            'city_address',
            'exact_address',
            'postal_code',
            'order_notes',
        ]

class ProfileFormBasic(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'national_number',
            'email',
            'Receive_the_newsletter',
        ]
        widgets = {
            'Receive_the_newsletter': forms.CheckboxInput()
        }


class ProfileFormLocations(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'province_address',
            'city_address',
            'exact_address',
            'postal_code',
            'order_notes',
        ]

