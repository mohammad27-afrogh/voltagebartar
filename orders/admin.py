from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import gettext as _

from .models import Order, OrderItem, Profile
from .forms import SmsSendForm
from .sms_service import send_sms_to_number_users

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]

@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'display_order_id',
        'first_name',
        'phone_number',
        'national_number',
        'postal_code',
        'date_time_create',
        'is_paid',
        'status',
        'payment_price',
    ]

    def display_order_id(self, obj):
        return str(obj.id)
    display_order_id.shoit_discription = 'Order ID'

    autocomplete_fields = ['province_address', 'city_address', ]

    inlines = [
        OrderItemInline,
    ]

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'quantity',
        'price',
        'date_time_create',
    ]


@admin.action(description=_('Send desired SMS'))
def send_sms_action(model_admin, request, queryset):
    selected = request.POST.getlist(ACTION_CHECKBOX_NAME)

    if 'apply' in request.POST:
        form = SmsSendForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            numbers = queryset.values_list('phone_number', flat=True)

            numbers = [n for n in numbers if n]

            if not numbers:
                model_admin.message_user(
                    request,
                    _('phone number not found!'),
                    level=message.ERROR
                )

                return redirect(request.get_full_path())

            send_sms_to_number_users(numbers, message)

            model_admin.message_user(
                request,
                f"_('sms send to') {len(numbers)} _('people.')",
                level=message.SUCCESS,
            )

            return redirect(request.get_full_path())

    else:
        form = SmsSendForm()

    context = {
        'form': form,
        'title': _('send sms'),
        'selected': selected,
    }
        
    return render(request, 'admin/send_sms_action.html', context)


@admin.register(Profile)
class ProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
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
        'date_time_create',
        'date_time_modified',
        'Receive_the_newsletter'
    ]
    autocomplete_fields = ['province_address', 'city_address']
    actions = [send_sms_action]