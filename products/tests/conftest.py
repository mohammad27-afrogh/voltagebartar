import pytest

from django.utils import timezone
from decimal import Decimal

from products.models import Product, Discount, Category, Features, Brand, Comment


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
        base_price = Decimal('15000.00'),
        product_type ='SEED',
        commodity_status ='AVA',
        short_description = 'a beautiful rose seed',
        description = 'long description of the rose',
    )
