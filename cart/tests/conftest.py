from random import choice, randint

import pytest
from django.contrib.auth import get_user_model

from faker import Faker

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from product.models import Product
from cart.models import CartItem
from django.utils import timezone


fake = Faker()

CATEGORY_CHOICES = (
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
    ('mixed_use', 'Mixed Use'),
)

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def sample_product_data():
    category, _ = choice(CATEGORY_CHOICES)



    return {
        'name': fake.word(),
        'category': category,
        'brand': fake.company(),
        'description': fake.sentence(),
        'min_price': 1000,
        'max_price': 2000,
        'min_quantity': 1,
        'max_quantity': 3,
        'rating': randint(1, 5),
        'created_at': timezone.now()
    }

@pytest.fixture
def user():
    return User.objects.create_user(username=fake.user_name(), password=fake.password())

@pytest.fixture
def logged_in_user_token(user):
    access_token = AccessToken.for_user(user)

    return str(access_token)

@pytest.fixture
def cart(user):
    return user.cart

@pytest.fixture
def product(sample_product_data):
    return Product.objects.create(**sample_product_data)

@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=fake.random_int(min=1, max=10))

