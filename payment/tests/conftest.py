import pytest
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth import get_user_model

from orders.models import Order, OrderItem
from locations.models import Province, City
from products.models import Product, Category, Features, Brand


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username = 'testeruser',
        password = 'password123456',
        email = 'userpayment@test.com'
    )

@pytest.fixture
def province():
    return Province.objects.create(
    name = 'Province Test',
)

@pytest.fixture
def city(province):
    return City.objects.create(
    province = province,
    name = 'تهران',
)

@pytest.fixture
def another_city(province):
    return City.objects.create(
        province = province,
        name = 'Another City',
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name ='Flowers',
        slug ='flower',
    )

@pytest.fixture
def features():
    return Features.objects.create(
        name_features = 'Standard_Dimensions',
        weight = Decimal('500.00'),
        weight_unit = 'GR',
    )

@pytest.fixture
def brand():
    return Brand.objects.create(
        name = 'Electric',
        description = 'This is a Brand Electric',
    )


@pytest.fixture
def product_instance(category, features, brand):
    return Product.objects.create(
        name = 'Rose_Seedling',
        slug = 'rose_seedling',
        sku = 'RS_001',
        category = category,
        features = features,
        brand = brand,
        base_price = '15000',
        product_type ='SEED',
        commodity_status ='AVA',
        short_description = 'a beautiful rose seed',
        description = 'long description of the rose',
    )


@pytest.fixture
def order(province, city, user, product_instance):
    created_order = Order.objects.create(
        user = user,
        first_name = 'Test',
        last_name = 'User',
        phone_number = '+989123456789',
        national_number = '1234567890',
        province_address = province,
        city_address = city,
        exact_address = 'Exact Address Test',
        postal_code = '1234567890',
        email = 'testuser@test.com',
        order_notes = 'Test Notes',
        payment_price = 'PP',
        is_paid = False,
        status = 'PEN',
        zarinpal_authority = '',
        zarinpal_ref_id = '',
    )

    OrderItem.objects.create(
        order=created_order, 
        product=product_instance, 
        quantity=2, 
    )

    created_order.refresh_from_db()
    return created_order


@pytest.fixture
def order_with_shiping_cost(province, another_city, user, product_instance):
    created_order = Order.objects.create(
        user = user,
        first_name = 'Shiping',
        last_name = 'User',
        phone_number = '+989123456789',
        national_number = '1234567890',
        province_address = province,
        city_address = another_city,
        exact_address = 'Exact Address Test',
        postal_code = '1234567890',
        email = 'shipinguser@test.com',
        order_notes = 'Shiping Notes',
        payment_price = 'PP',
        is_paid = False,
        status = 'PEN',
        zarinpal_authority = '',
        zarinpal_ref_id = '',
    )

    OrderItem.objects.create(
        order=created_order,
        product=product_instance, 
        quantity=2,
    )

    created_order.refresh_from_db()
    return created_order
