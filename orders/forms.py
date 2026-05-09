from django import forms
from django.utils.translation import gettext as _
from dal import autocomplete

from .models import Order, Profile
from locations.models import Province, City

class AddressFormOrder(forms.Form):
    PYMENT_PRICE_CHOICESS = [
        ('PP', _('Pyment Price')),
        ('HD', _('House Door')),
    ]

    payment_price = forms.ChoiceField(label=_('pyment_price'), required=True, choices=[('', _('choose how to pay...'))] + PYMENT_PRICE_CHOICESS)
    first_name = forms.CharField(max_length=50, label=_('first_name'), required=True)
    last_name = forms.CharField(max_length=50, label=_('last_name'), required=True)
    phone_number = forms.CharField(max_length=15, label=_('phone_number'), required=True)
    national_number = forms.CharField(max_length=10, label=_('national_number'), required=True) 
    postal_code = forms.CharField(max_length=10, label=_('postal code'), required=True) 
    # فیلد استان با ویجت autocomplete
    province_address = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=autocomplete.ModelSelect2(url='locations:province_autocomplete', attrs={
            'data-placeholder': _('search the province for interest...'),
            'data-minimum-input-length': 1,
        }),
        label=_('province'),
        required=True
    )

    # فیلد شهر با ویجت autocomplete
    # از 'forward' برای ارسال مقدار استان انتخاب شده استفاده میکنیم
    city_address = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='locations:city_autocomplete',
            forward={
                'province_address',
            },
            attrs={
                'data-placeholder': _("select the province first..."),
                'data-minimum-input-length': 1,
                'data-disable-clearable': True,
            },
        ),
        label=_('city'),
        required=True
    )
    
    exact_address = forms.CharField(widget=forms.Textarea, label=_('exact_address'), required=True)
    email = forms.EmailField(label=_('email'), required=True)
    order_notes = forms.CharField(widget=forms.Textarea, required=False, label=_('order notes'))

    # اضافه کردن متد save اگر نیاز دارید داده ها را در مدل Order ذخیره کنید
    def save(self, commit=True):
        order_data = self.cleaned_data
        # استخراج داده ها از cleaned_data
        payment_method = order_data.get('payment_price')
        first_name = order_data.get('first_name')
        last_name = order_data.get('last_name')
        phone_number = order_data.get('phone_number')
        national_number = order_data.get('national_number')
        postal_code = order_data.get('postal_code')
        province = order_data.get('province_address')
        city = order_data.get('city_address')
        exact_address = order_data.get('exact_address')
        email = order_data.get('email')
        order_notes = order_data.get('order_notes')

        # ایجاد یا به روز رسانی شیء Order
        order = Order() # یا Order.objects.get(pk=...) برای ویرایش
        order.payment_price = payment_method
        order.first_name = first_name
        order.last_name = last_name
        order.phone_number = phone_number
        order.national_number = national_number
        order.email = email
        order.province_address = province
        order.city_address = city
        order.exact_address = exact_address
        order.postal_code = postal_code
        order.order_notes = order_notes

        if commit:
            order.save()
        return order


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


class SmsSendForm(forms.Form):
    message = forms.CharField(label=_('text sms...'))
    widget = forms.Textarea(attrs={
        'rows': 5,
        'cols': 60,
        'placeholder': _('Enter the message text...'),
    })