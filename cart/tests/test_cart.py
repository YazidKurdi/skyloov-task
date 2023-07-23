import pytest
from django.urls import reverse
from rest_framework import status

from cart.models import CartItem



@pytest.mark.django_db
def test_add_product_to_cart_anonymous_client(client, cart, product):
    url = reverse('add-product')

    data = {
        'product_id': product.id,
        'quantity': 2,
    }

    response = client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'error' in response.data

@pytest.mark.django_db
def test_add_product_to_cart_auth_client(client,logged_in_user_token, cart, product):
    url = reverse('add-product')


    data = {
        'product_id': product.id,
        'quantity': 2,
    }

    response = client.post(url, data,HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_cart_model_properties(client,logged_in_user_token, cart, product):
    url = reverse('add-product')


    data = {
        'product_id': product.id,
        'quantity': 2,
    }

    response = client.post(url, data,HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")
    assert cart.num_of_items == data['quantity']
    assert cart.cart_total == data['quantity'] * product.min_price



@pytest.mark.django_db
def test_delete_cart_item(client, logged_in_user_token, cart, product):

    url_add_product = reverse('add-product')
    data = {
        'product_id': product.id,
        'quantity': 2,
    }
    client.post(url_add_product, data, HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")


    url_delete_cart_item = reverse('delete-product')

    data = {
        'product_id': product.id,
    }

    response = client.delete(url_delete_cart_item, data, content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CartItem.objects.filter(cart=cart, product=product).count() == 0

    response = client.delete(url_delete_cart_item, data, content_type='application/json',
                             HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_cart_item(client, logged_in_user_token, cart, product):

    url_add_product = reverse('add-product')
    data = {
        'product_id': product.id,
        'quantity': 2,
    }
    client.post(url_add_product, data, HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")


    url_update_cart_item = reverse('update-product')

    updated_quantity = 5
    update_data = {
        'product_id': product.id,
        'quantity': updated_quantity,
    }

    response = client.put(url_update_cart_item, update_data, content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")

    assert response.status_code == status.HTTP_200_OK
    assert CartItem.objects.filter(cart=cart, product=product, quantity=updated_quantity).exists()

@pytest.mark.django_db
def test_update_cart_item_invalid_data(client, logged_in_user_token, cart, product):

    url_add_product = reverse('add-product')
    data = {
        'product_id': product.id,
        'quantity': 2,
    }
    client.post(url_add_product, data, HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")


    url_update_cart_item = reverse('update-product')

    invalid_data = {

        'quantity': 5,
    }

    response = client.put(url_update_cart_item, invalid_data, content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data


@pytest.mark.django_db
def test_retrieve_cart_unauthenticated(client):

    url_retrieve_cart = reverse('retrieve-products')

    response = client.get(url_retrieve_cart)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data


@pytest.mark.django_db
def test_retrieve_empty_cart_on_user_signup_authenticated(client, logged_in_user_token, cart, product):

    url_retrieve_cart = reverse('retrieve-products')

    response = client.get(url_retrieve_cart, HTTP_AUTHORIZATION=f"Bearer {logged_in_user_token}")


    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.data
    assert 'owner' in response.data
    assert 'created_at' in response.data
    assert 'num_of_items' in response.data
    assert 'cart_total' in response.data
    assert 'cart_items' in response.data
    assert response.data['num_of_items'] == 0
    assert response.data['cart_total'] == 0
    assert len(response.data['cart_items']) == 0

