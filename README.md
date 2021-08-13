# TopStore

SoftUni - Python Web Framework End Project


## Overview

TopStore is an Ecommerce store web application built on Django MTV (Model, Template, View) architecture.

Version control system - Git.

PostgreSQL DB.

Function Based Views.

20 endpoints.

Template inheritance.

Responsive design.

Error Handling and Data Validations.

Unit Tests.

Extended Django user.

Several types of users functionality.

**Unauthenticated Users** - Can leave a contact message to the staff, if name and email are correctly provided.

They can also view the store/, contact/, about/, product/all/ and product/details/ pages.


**Common Authenticated Users** - They can like, review, add or remove products from their cart and complete an order. 

They can also check their order history and leave a contact message to the staff.


**TopStore Staff Users** - Have full CRUD functionality over the added products in the admin section and in the user section of the app.

They can check the TopStore users, contact messages and all the products and orders.


**Admin Users** - Have full CRUD functionality over the app.


**How to make an account?**

You can create an account through /account/register/ if Email, Username and Password are correctly provided.

Or you can use manage.py.

## Video Presentation

[![Video Presentation](https://github.com/dimitar-daskalov/TopStore/blob/main/static/images/overview.png)](https://youtu.be/nEdcXNyJavA)

## Installation

**First**
```bash
git clone https://github.com/dimitar-daskalov/TopStore
```
**Then**
```bash
pip install -r requirements.txt
```
## In order to use the app, you should:

Change django secret key in settings.py

```python
SECRET_KEY = environ.get('SECRET_KEY') # - change to a valid secret key
```

Change database credentials.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'), # - change to a valid database name
        'USER': environ.get('DB_USER'), # - change to a valid db username
        'PASSWORD': environ.get('DB_PASSWORD'), # - change to a valid db password
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

or use the default :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## License

[MIT](https://github.com/dimitar-daskalov/TopStore/blob/main/LICENSE)
