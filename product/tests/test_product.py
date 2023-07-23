import pytest
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient

from product.models import Product
from product.serializers import ProductSerializer


@pytest.mark.django_db
def test_single_product_list_view(client, sample_product_data):

    Product.objects.create(**sample_product_data)

    url = reverse('product-list-create')


    response = client.get(url)


    assert response.status_code == status.HTTP_200_OK


    assert response.data.get('count') == 1

    assert response.data.get('results')[0]['name'] == sample_product_data['name']
    assert response.data.get('results')[0]['category'] == sample_product_data['category']
    assert response.data.get('results')[0]['brand'] == sample_product_data['brand']
    assert round(float(response.data.get('results')[0]['min_price'])) == round(float(sample_product_data['min_price']))
    assert round(float(response.data.get('results')[0]['max_price'])) == round(float(sample_product_data['max_price']))
    assert round(float(response.data.get('results')[0]['min_quantity'])) == round(float(sample_product_data['min_quantity']))
    assert round(float(response.data.get('results')[0]['max_quantity'])) == round(float(sample_product_data['max_quantity']))
    assert response.data.get('results')[0]['rating'] == sample_product_data['rating']


    assert round(float(response.data.get('results')[0]['min_quantity'])) <= round(float(sample_product_data['max_quantity']))
    assert round(float(response.data.get('results')[0]['min_price'])) <= round(float(sample_product_data['max_price']))

@pytest.mark.django_db
def test_multiple_product_list_view(client,sample_product_data):
    for _ in range(2):
        Product.objects.create(**sample_product_data)

    url = reverse('product-list-create')


    response = client.get(url)


    assert response.status_code == status.HTTP_200_OK


    assert response.data.get('count') == 2

@pytest.mark.django_db
def test_post_request_product_non_authenticated(client, sample_product_data):

    serializer = ProductSerializer(data=sample_product_data)


    assert serializer.is_valid(), serializer.errors

    url = reverse('product-list-create')

    response = client.post(url, serializer.validated_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_post_request_product_authenticated(client, logged_in_user_token, sample_product_data):


    serializer = ProductSerializer(data=sample_product_data)

    assert serializer.is_valid(), serializer.errors

    url = reverse('product-list-create')
    response = client.post(url, serializer.validated_data, HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}",)


    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_get_request_product_search_by_description(client, sample_product_data):

    description_list = ['Luxury Apartment','Luxury House']

    description_to_search = 'Luxury'

    for description in description_list:
        sample_product_data['description'] = description
        Product.objects.create(**sample_product_data)

    url = reverse('product-list-create')


    response = client.get(url, {'search': description_to_search})


    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('count') == 2


@pytest.mark.django_db
def test_get_request_ordering_by_rating_asc(client,sample_product_data):
    for _ in range(3):
        Product.objects.create(**sample_product_data)

    url = reverse('product-list-create')


    response = client.get(url, {'ordering': 'rating'})


    assert response.status_code == 200
    results = response.data
    assert results.get('count') == 3
    assert results.get('results')[0]['rating'] <= results.get('results')[1]['rating'] <= results.get('results')[2]['rating']

@pytest.mark.django_db
def test_get_request_ordering_by_rating_desc(client,sample_product_data):
    for _ in range(3):
        Product.objects.create(**sample_product_data)

    url = reverse('product-list-create')


    response = client.get(url, {'ordering': 'rating'})


    assert response.status_code == 200
    results = response.data
    assert results.get('count') == 3
    assert results.get('results')[0]['rating'] >= results.get('results')[1]['rating'] >= results.get('results')[2]['rating']


@pytest.mark.django_db
def test_get_request_product_filter_by_name(client, sample_product_data):
    for _ in range(2):
        sample_product_data['category'] = 'residential'
        Product.objects.create(**sample_product_data)


    url = reverse('product-list-create')


    response = client.get(url, {'category': 'residential'})


    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('count') == 2