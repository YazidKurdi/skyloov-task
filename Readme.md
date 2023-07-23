
# Skyloov Backend Assigment

This Django backend project aims to provide a robust API for managing products, with features such as searching for products based on category and price range, authentication using JWT, pagination, sorting, API documentation with Swagger, and image upload with parallel processing. Additionally, the project includes the implementation of Celery for background tasks, specifically sending emails to new users after 1 day (10 seconds used for development) of registration. The final application will be deployed using Docker.


## Installation

Clone the repository locally & cd into the directory

```
git clone https://github.com/YazidKurdi/skyloov-task.git && cd skyloov-task
```

#### Running the backend server (Docker), run the below commands in the main project directory using separate terminals for python and celery

1. Pull the docker images and spin up the containers:
```
docker-compose up
```

2. Visit  http://127.0.0.1:8000
## Features

### Login & Signup
- Signing up automatically creates a cart using signals
- JWT authentication (token & refresh)

### Product
- Product creation
- Product retrieval (Filter, search and ordering enabled)

### Cart
- Perform CRUD operations adding products to cart
- Cart properties (number of items in cart & total dollar amount of cart items)

### Account
- An automated welcome email is sent after 10 seconds from signing up
- Activation email is sent to user to activate account enabling access to backend resources

### Misc
- Documentation using Swagger (drf_yasg package) @ http://127.0.0.1:8000/swagger/ - Login to recieve access token and paste in "Authorization" box
- Multi threading image processing to various sizes







## Unit Testing (Locally)

Run ```docker-compose exec web pytest``` while in the main project directory
