import django
import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.utils import timezone

from random import choice, uniform, randint

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

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

    min_price = round(uniform(0, 1000),2)
    max_price = round(uniform(0, 1000),2)
    if min_price > max_price:
        min_price, max_price = max_price, min_price

    min_quantity = round(randint(1, 100),2)
    max_quantity = round(randint(1, 100),2)
    if min_quantity > max_quantity:
        min_quantity, max_quantity = max_quantity, min_quantity


    return {
        'name': fake.word(),
        'category': category,
        'brand': fake.company(),
        'description': fake.sentence(),
        'min_price': min_price,
        'max_price': max_price,
        'min_quantity': min_quantity,
        'max_quantity': max_quantity,
        'rating': randint(1, 5),
        'created_at': timezone.now()
    }

@pytest.fixture
def logged_in_user_token():
    # Create a user account
    user_data = {
        'username': 'testuser',
        'password': 'testpassword',
    }
    user = User.objects.create_user(**user_data)

    access_token = AccessToken.for_user(user)

    return str(access_token)