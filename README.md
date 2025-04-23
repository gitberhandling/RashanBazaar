# Rashan Bazar – Your Trusted Grocery Partner

An online grocery shopping platform built with Django and modern web technologies.

## Features

- User authentication and profile management
- Product browsing and search functionality
- Shopping cart and checkout system
- Order tracking and management
- Discount and promotion system
- Customer support system

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

- `rashan_bazar/` - Main project directory
  - `accounts/` - User authentication and profile management
  - `products/` - Product catalog and management
  - `cart/` - Shopping cart functionality
  - `orders/` - Order processing and tracking
  - `static/` - Static files (CSS, JavaScript, images)
  - `templates/` - HTML templates

## Technology Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (development) / MySQL (production)
- Authentication: django-allauth
- Forms: django-crispy-forms
- Payment Processing: Stripe 