from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_cards_invalid(auth_client, board, list):
    """
    User cannot create cards without required data.
    """

    response = auth_client.post(reverse('cards', args=[board.id, list.id]))

    assert response.status_code == 400
    assert 'title' and 'order' in response.data


@pytest.mark.django_db
def test_cards_unauthorized(auth_client2, board, client, list, titles):
    """
    Unauthorized user cannot list or create cards.
    """

    client.credentials()

    response_unauthenticated_create = client.post(reverse('cards', args=[board.id, list.id]), {
        'title': titles['card'],
        'order': 1
    })
    response_unauthenticated_list = client.post(reverse('cards', args=[board.id, list.id]))
    response_unauthorized_create = auth_client2.post(reverse('cards', args=[board.id, list.id]), {
        'title': titles['card'],
        'order': 1
    })
    response_unauthorized_list = auth_client2.post(reverse('cards', args=[board.id, list.id]))
    responses = [
        response_unauthenticated_create,
        response_unauthenticated_list,
        response_unauthorized_create,
        response_unauthorized_list
    ]

    assert all(i.status_code == 401 for i in responses)
    assert all(i.data['detail'].code == 'not_authenticated' for i in responses)


@pytest.mark.django_db
def test_cards_success(auth_client, board, list, titles, titles2):
    """
    Authorized user can list and create cards.
    """

    response_create = auth_client.post(reverse('cards', args=[board.id, list.id]), {
        'title': titles['card'],
        'order': 1
    })
    response_create2 = auth_client.post(reverse('cards', args=[board.id, list.id]), {
        'title': titles2['card'],
        'order': 2
    })
    response_list = auth_client.get(reverse('cards', args=[board.id, list.id]))

    assert response_create.status_code == 201
    assert response_create2.status_code == 201
    assert response_list.status_code == 200
    assert response_create.data['title'] == titles['card']
    assert response_create2.data['title'] == titles2['card']
    assert response_create.data['order'] == 1
    assert response_create2.data['order'] == 2
    assert len(response_list.data) == 2


@pytest.mark.django_db
def test_card_invalid(auth_client, board, card, list):
    """
    User cannot update cards with blank data.
    """

    response = auth_client.put(reverse('card', args=[board.id, list.id, card.id]), {'title': '', 'order': ''})

    assert response.status_code == 400
    assert 'title' and 'order' in response.data


@pytest.mark.django_db
def test_card_unauthorized(auth_client2, board, card, client, list):
    """
    Unauthorized user cannot retrieve, update, or delete cards.
    """

    client.credentials()

    response_unauthenticated = client.get(reverse('card', args=[board.id, list.id, card.id]))
    response_unauthorized = auth_client2.get(reverse('card', args=[board.id, list.id, card.id]))
    responses = [response_unauthenticated, response_unauthorized]

    assert all(i.status_code == 401 for i in responses)
    assert all(i.data['detail'].code == 'not_authenticated' for i in responses)


@pytest.mark.django_db
def test_card_success(auth_client, board, card, list, titles2):
    """
    Authorized user can retrieve, update, and delete cards.
    """

    response_retrieve = auth_client.get(reverse('card', args=[board.id, list.id, card.id]))
    response_update = auth_client.put(reverse('card', args=[board.id, list.id, card.id]), {
        'title': titles2['card'],
        'order': 2
    })
    response_delete = auth_client.delete(reverse('card', args=[board.id, list.id, card.id]))

    assert response_retrieve.status_code == 200
    assert response_update.status_code == 200
    assert response_delete.status_code == 204
    assert response_retrieve.data['id'] == card.id
    assert response_retrieve.data['title'] == card.title
    assert response_retrieve.data['order'] == card.order
    assert response_update.data['title'] == titles2['card']
    assert response_update.data['order'] == 2
