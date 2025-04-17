# Food Orders Q

A full-featured food delivery web application that allows customers to browse menu items, place orders, and track delivery while enabling restaurant owners to manage inventory and process orders efficiently.

## Project Overview

This project was developed during an internship at Prepway Solutions Pvt Ltd. Food Orders Q is a comprehensive food ordering platform designed to streamline the process of online food ordering and delivery management.

## Features

- **User Authentication:** Secure login and registration system with user profiles
- **Menu Management:** Admin interface to add, update, and remove menu items
- **Shopping Cart:** Real-time cart functionality for adding and removing items
- **Order Processing:** Complete order workflow from placement to delivery
- **Admin Dashboard:** Comprehensive dashboard for restaurant owners to manage orders
- **Responsive Design:** Mobile-friendly interface that works on all devices

## Technologies Used

- **Backend:** Django (Python web framework)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Deployment:** Gunicorn, WhiteNoise
- **Version Control:** Git
- **Hosting:** Render

## Installation and Setup

1. Clone the repository
   ```
   git clone https://github.com/baihelahusain/food-orders-q.git
   cd food-orders-q
   ```

2. Create a virtual environment and activate it
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Deployment

The application is deployed on Render and can be accessed at [https://food-orders-q.onrender.com/](https://food-orders-q.onrender.com/)

## Project Structure

- `food/` - Main application containing models, views, and templates for food ordering
- `users/` - Authentication and user profile management
- `foodsite/` - Django project settings
- `static/` - Static files (CSS, JavaScript, images)
- `templates/` - HTML templates

## Contributors

- Baihela Hussain - Project Developer

## Acknowledgments

- Prepway Solutions Pvt Ltd for providing the internship opportunity
- Mentors and staff for their guidance and support throughout the project

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 Food Orders Q. Created by Baihela Hussain. All rights reserved.
