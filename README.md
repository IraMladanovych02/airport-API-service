# Airport API Service

Welcome to the **Airport API Service**!

The Airport API is a RESTful web service designed for managing airport-related information, enabling users to efficiently manage planes, users, orders, tickets, and more.


## Features

- **User Management**: Create and manage user accounts.
- **Plane Management**: Manage information related to airport(planes, orders, services, etc).


**Also you can find project mapping in folder "doc"**

## Installation

Before getting started with the Airport API Service, ensure that you have Python installed on your system. If Python is not installed, you can download and install it from the official [Python website](https://www.python.org/downloads/).

Once Python is installed, follow these steps to set up the Airport API Service:

1. Clone the repository:
   ```bash
   git clone https://github.com/IraMladanovych02/airport-API-service.git

2. Create a virtual environment:
   ```bash
   python -m venv venv

3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate (on Windows)
   source venv/bin/activate (On macOS/Linux)

4. Install the required packages:
   ```bash
   pip install -r requirements.txt

5. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. Create a superuser
   ```bash
   python manage.py createsuperuser

7. Start the development server:
   ```bash
   python manage.py runserver
   