# TopStore

SoftUni - Python Web Framework End Project


## Overview

TopStore is a Ecommerce store web application which simulates ecommerce store platform.

Implemented using Django Framework.

Source control system - Github.

PostgreSQL DB.

Function Based Views.

20 endpoints

Template inheritance.

Error Handling and Data Validations.

Tests included.

Login/register.

Extended Django user.

Several types of users functionality.

**Unauthenticated Users** - Can leave a contact message to the staff, if name and email is provided.

They can also see the store/, contact/, about/, product/all/ and product/details/ pages.


**Normal Authenticated Users** - They can like, review, add products to their cart and complete a checkout. 

They can also check their order history and leave a contact message to the staff.


**TopStore Staff Users** - Have full CRUD functionality over the added products in the admin section and in the user section of the app.

They can check the TopStore users, contact messages and all the products and orders.


**Admin Users** - Have full CRUD functionality over the app.


**How to make an account?**

You can make account through /account/register/ if Email, Username and Password are correctly provided.

Or you can make account with manage.py.


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
