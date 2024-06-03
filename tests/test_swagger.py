# Imports
from http import HTTPStatus

import pytest
from django.urls import reverse


# Function to check if swagger schema is accessible by admin
def test_swagger_schema_accessible_by_admin(admin_client):
    url = reverse("swagger--schema", kwargs={"format": ".json"})
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


# Function to check if swagger schema is accessible by normal user
@pytest.mark.django_db()
def test_swagger_schema_accessible_by_normal_user(client):
    url = reverse("swagger--schema", kwargs={"format": ".json"})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Function to check if swagger UI is accessible by admin
def test_swagger_ui_accessible_by_admin(admin_client):
    url = reverse("swagger--playground")
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


# Function to check if swagger UI is accessible by normal user
@pytest.mark.django_db()
def test_swagger_ui_accessible_by_normal_user(client):
    url = reverse("swagger--playground")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Function to check if redoc is accessible by admin
def test_redoc_accessible_by_admin(admin_client):
    url = reverse("swagger--redoc")
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


# Function to check if redoc is accessible by normal user
@pytest.mark.django_db()
def test_redoc_accessible_by_normal_user(client):
    url = reverse("swagger--redoc")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
