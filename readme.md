# 🔑 Vendor Management System

## Django / Django Rest Framework Based Vendor Management System

[![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-092E20?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Django CORS Headers](https://img.shields.io/badge/-Django%20CORS%20Headers-092E20?style=flat&logo=django&logoColor=white)](https://github.com/adamchainz/django-cors-headers)
[![Django Extensions](https://img.shields.io/badge/-Django%20Extensions-092E20?style=flat&logo=django&logoColor=white)](https://django-extensions.readthedocs.io/en/latest/)
[![Django Jazzmin Dashboard](https://img.shields.io/badge/-Django%20Jazzmin%20Dashboard-092E20?style=flat&logo=django&logoColor=white)](https://django-jazzmin.readthedocs.io/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![OpenAPI Swagger UI](https://img.shields.io/badge/-OpenAPI%20Swagger%20UI-85EA2D?style=flat&logo=swagger&logoColor=black)](https://github.com/axnsan12/drf-yasg)
[![Argon2](https://img.shields.io/badge/-Argon2-092E20?style=flat&logo=argon&logoColor=white)](https://github.com/hynek/argon2-cffi)
[![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/-Celery-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/)
[![Celery Beat](https://img.shields.io/badge/-Celery%20Beat-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
[![Flower](https://img.shields.io/badge/-Flower-37814A?style=flat&logo=flower&logoColor=white)](https://flower.readthedocs.io/en/latest/)
[![PyTest](https://img.shields.io/badge/-PyTest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/en/latest/)
[![Werkzeug](https://img.shields.io/badge/-Werkzeug-D84924?style=flat&logo=werkzeug&logoColor=white)](https://werkzeug.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)


<hr />

## 🔓 Core

The `core` app provides a custom-built query parameter token authentication system for secure user authentication and authorization. It leverages JSON Web Tokens (JWT) to ensure robust and scalable authentication mechanisms.


## 👤 Users

The `users` app houses a custom-built User model, tailored to meet the specific requirements of the Vendor Management System. It also includes API endpoints for listing and retrieving user information, enabling efficient user management.

## 🏢 Vendors

The `vendors` app encompasses the Vendor model and associated API endpoints for CRUD (Create, Read, Update, Delete) functionality. It allows for seamless management of vendor information and records, including overall vendor performance tracking.

## 📝 Purchase Orders

The `purchase_order` app manages the Purchase Order model and provides API endpoints for CRUD operations on purchase orders. It also includes endpoints for effectively controlling the flow of purchase orders and accurately recording timestamps. Additionally, signals are implemented to control order dates and statuses automatically.

## 📈 Historical Performance

The `historical_performance` app records and maintains historical performance data for vendors. It leverages Celery Beat, a periodic task scheduler, to record historical performance records every 6 hours, ensuring up-to-date and comprehensive vendor performance tracking.


<hr />

## Required Environment Variables

To ensure proper configuration and deployment of the Vendor Management System, the following environment variables must be set up.

1. Create a `.env` file at the location of `manage.py` and populate it with the required values:

```text
# Django settings module to be used by the application.
DJANGO_SETTINGS_MODULE=

# Flag to indicate if Django should read the .env file.
DJANGO_READ_DOT_ENV_FILE=

# Enables or disables Django's debug mode.
DJANGO_DEBUG=

# Secret key used by Django for cryptographic signing.
DJANGO_SECRET_KEY=

# URL for connecting to the Redis service, used for caching and Celery message broker.
REDIS_URL=

# URL for connecting to the PostgreSQL database.
DATABASE_URL=

# URL for the Celery message broker, using Redis.
CELERY_BROKER_URL=

# Celery flower user and password
CELERY_FLOWER_USER=
CELERY_FLOWER_PASSWORD=

# PostgreSQL database settings.
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

2. Create a `.envs` folder at the location of `manage.py` and in it create `.env.django` and populate it with the required values:

```text
# Django settings module to be used by the application.
DJANGO_SETTINGS_MODULE=

# Flag to indicate if Django should read the .env file.
DJANGO_READ_DOT_ENV_FILE=

# Enables or disables Django's debug mode.
DJANGO_DEBUG=

# Secret key used by Django for cryptographic signing.
DJANGO_SECRET_KEY=

# URL for connecting to the Redis service, used for caching and Celery message broker.
REDIS_URL=

# URL for connecting to the PostgreSQL database.
DATABASE_URL=

# URL for the Celery message broker, using Redis.
CELERY_BROKER_URL=

# Celery flower user and password
CELERY_FLOWER_USER=
CELERY_FLOWER_PASSWORD=
```

3. Create a `.envs` folder at the location of `manage.py` and in it create `.env.postgres` and populate it with the required values:

```text
# PostgreSQL database settings.
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```


<hr />

# API Endpoints

## Core App

- `POST /obtain-auth-token/` - API Key Token for User Authentication

## Users

- `GET /users/` - List all users
- `GET /users/<email>/` - Retrieve a specific user

## Vendors

- `GET /vendors/` - List all vendors
- `POST /vendors/` - Create a new vendor
- `GET /vendors/{vendor_code}/` - Retrieve a specific vendor
- `PUT /vendors/{vendor_code}/` - Update a vendor
- `DELETE /vendors/{vendor_code}/` - Delete a vendor

## Purchase Orders
- `GET /purchase-orders/` - List all purchase orders
- `POST /purchase-orders/` - Create a new purchase order
- `GET /purchase-orders/<po_number>/` - Retrieve a specific purchase order
- `PUT /purchase-orders/<po_number>/` - Update a purchase order
- `DELETE /purchase-orders/<po_number>/` - Delete a purchase order

## Purchase Order Status Operations
- `POST /purchase-orders/<po_number>/issue/` - Issue a purchase order to a vendor
- `POST /purchase-orders/<po_number>/acknowledge/` - Acknowledge a purchase order
- `POST /purchase-orders/<po_number>/deliver/` - Deliver a purchase order
- `POST /purchase-orders/<po_number>/cancel/` - Cancel a purchase order
- `POST /purchase-orders/<po_number>/rate-quality/` - Assign a value for rate_quality of the purchase order
