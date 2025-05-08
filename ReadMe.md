Django eCommerce Platform

An eCommerce web application built with Django, supporting vendor and buyer roles.
Vendors can manage stores and products, while buyers can browse, add products to their cart, checkout, and leave reviews.

Features

User Roles
- Vendors:
  - Register and log in as vendors
  - Create and manage stores
  - Add, edit, and delete products within their stores

- Buyers:
  - Register and log in as buyers
  - Browse stores and products
  - Add products to a cart (session-based)
  - Checkout and receive an email invoice
  - Leave reviews on purchased products (verified reviews) or without purchase (unverified reviews)

Shopping Cart
- Session-based cart (no login required)
- Update item quantities
- Remove items

Checkout
- Checkout page to review cart and confirm purchase
- Upon successful checkout:
  - Products are recorded in a Purchase model
  - Invoice sent to buyer's email

Reviews
- Buyers can leave:
  - Verified reviews (if they purchased the product)
  - Unverified reviews (if they have not)
- Reviews are displayed on the product detail page

Authentication
- Role-based login and registration (vendor or buyer)
- Password reset via email with token expiration

Admin Panel
- Django admin panel available for managing users, stores, products, purchases, and reviews

Tech Stack
- Backend: Django 4.x
- Database: MySQL (managed via HeidiSQL)
- Frontend: Django templates with Bootstrap 5 styling
- Email: Django's email backend (for password reset and invoice emails)

Setup Instructions

1. Clone the repository:
   git clone https://github.com/ZondoJnr/caleb-ecommerce-django-web-app.git
   cd caleb-ecommerce-django-web-app

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Configure database in settings.py:
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }

5. Run migrations:
   python manage.py migrate

6. Create a superuser:
   python manage.py createsuperuser

7. Start the development server:
   python manage.py runserver

8. Access the site:
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

Folder Structure

ecommerce/
├── shop/
│   ├── templates/
│   │   ├── shop/
│   │   ├── registration/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── ecommerce/ (project settings)
├── manage.py
├── requirements.txt
└── README.md

Future Improvements
- Stripe or PayPal integration for real payments
- Product search and filtering
- Wishlist feature for buyers
- Multi-image product galleries
- Storefront themes for vendors
