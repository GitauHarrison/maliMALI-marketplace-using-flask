![GitHub Open Issues](https://img.shields.io/github/issues/GitauHarrison/maliMALI-marketplace-using-flask) ![GitHub Closed Issues](https://img.shields.io/github/issues-closed/GitauHarrison/maliMALI-marketplace-using-flask) ![GitHub Pull Request Open](https://img.shields.io/github/issues-pr/GitauHarrison/maliMALI-marketplace-using-flask) ![GitHub Pull Request Closed](https://img.shields.io/github/issues-pr-closed/GitauHarrison/maliMALI-marketplace-using-flask) ![GitHub forks](https://img.shields.io/github/forks/GitauHarrison/maliMALI-marketplace-using-flask) ![GitHub Stars](https://img.shields.io/github/stars/GitauHarrison/maliMALI-marketplace-using-flask)


# maliMALI Marketplace

![eCommerce App](/app/static/images/sample_ecommerce_app.gif)

## Overview

This is a basic eCommerce app. Vendors can sell items on the platform while customers can shop for these items. Card and MPesa Payment integration is added to complete the purchase cycle. 

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
|     [drawSQL](https://drawsql.app/teams/gitau-harrison/diagrams/sample-ecommerce-app)      |	[Figma](https://www.figma.com/proto/3R0RquHDmlfeN9m954BjF4/sample-eCommerce-app?node-id=2%3A616&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=1%3A2)       |	[Render](https://sample-ecommerce-app.onrender.com/)   |	      [![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/sample-ecommerce-app-using-flask)](https://github.com/GitauHarrison/sample-ecommerce-app-using-flask/graphs/contributors)  |	~~[Tests](test_web_app.py)~~ |

## Application Details

Application users:

- Admin
    - Creates the vendors after verifying their details
    - Only an admin can add a vendor
    - The assumption here is that the admin verifies the vendor before onboarding

- Vendor:
    - Creates products he wants to sell

- Customer:
    - Purchases products they want

To test the live app, use these credentials (if you don't want to create your own):

- Admin:
    - Username: **harry**
    - Password: **ecommerceapp123**

- Vendor:
    - Username: **tanya**
    - Password: **ecommerceapp123**

- Customer:
    - Username: **taste**
    - Password: **ecommerceapp123**


## Testing It Locally

- Clone this repo:

    ```python
    $ git clone git@github.com:GitauHarrison/maliMALI-marketplace-using-flask.git
    ```

- Change directory into the cloned repo:

    ```python
    $ cd maliMALI-marketplace-using-flask
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


[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](https://forthebadge.com)