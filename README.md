# Sample eCommerce App

![eCommerce App](/app/static/images/sample_ecommerce_app.gif)

## Overview

This is a basic eCommerce app. The main goal is to allow customers to shop for items near them at a discount. The application is able to know where a customer is located, and upon search, the customer can find vendors near him, and can take advantage of offers in his locality. Discounts vary depeding on location.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Additional Details](#additional-details)
- [Application Details](#application-details)
- [Testing It Locally](#testing-it-locally)


## Features
- [x] Basic user authentication
- [x] Database management
- [x] Lipa Na Mpesa (pay using Mpesa)
- [x] Get free airtime upon completing a purchase
- [ ] Geocomplete during search
- [ ] Find vendors near you


## Technologies Used
- Flask micro-framework
- Python, JavaScript for programming
- Lipa Na MPesa API
- Airtime API (Africa's Talking)
- Google Maps API
- SQLite for the database

## Additional Details

| Db Schema Design |	UI Design	| Deployment |	Contributors |	Tests |
| ---------------- | -------------- | ---------- | ------------- | ------ |
|     [drawSQL](https://drawsql.app/teams/gitau-harrison/diagrams/sample-ecommerce-app)      |	[Figma](https://www.figma.com/proto/3R0RquHDmlfeN9m954BjF4/sample-eCommerce-app?node-id=2%3A616&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=1%3A2)       |	[Render](https://sample-ecommerce-app.onrender.com/)   |	      [GitHub](https://github.com/GitauHarrison/sample-ecommerce-app-using-flask/graphs/contributors) |	[Tests](test_web_app.py) |

## Application Details

Application users:

- Admin
    - Creates the vendors after verifying their details

- Vendor:
    - Creates products he wants to sell

- Customer:
    - Purchases products they want

Majority of the functionality is developed to improve a customer's shopping experience. A customer can easily search for shops near him. The search query returns a list of vendors closest to him, adequately marked on the map. During checkout, a customer pays using the Lipa Na Mpesa service from Safaricom. Successful purchases sees that a customer receives free talking time top-up. This also happens to the vendor. The main objective is to appreciate both the vendor and the customer for using the platform.

## Testing It Locally

- Clone this repo:

    ```python
    $ git@github.com:GitauHarrison/sample-ecommerce-app-using-flask.git
    ```

- Change directory into the cloned repo:

    ```python
    $ cd sample-ecommerce-app-using-flask
    ```

- Create and activate a virtual environment

    ```python
    # Using virtualenvwrapper
    $ mkvirtualenv venv

    # Normal way
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

- Install needed dependancies:

    ```python
    (venv)$ pip3 install -r requirements.txt
    ```

- Add and update environment variables in a `.env` file as seen in `.env-template`:

    ```python
    (venv)$ cp .env-template .env
    ```

- Start the flask server:

    ```python
    (venv)$ flask run
    ```

- Check the application in your favourite browser by pasting http://127.0.0.1:5000.
