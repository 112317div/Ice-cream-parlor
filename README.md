Ice Cream Parlor Management System
A Python application to manage ice cream flavors, ingredients, and customer preferences using SQLite.

-->Features
Browse flavors by season
Search flavors by name or description
Add flavors to a shopping cart
Register customers with allergy information
Suggest new flavors
View ingredient inventory
Add and view allergens
Checkout system with total price calculation

-->Requirements
Python 3.6 or higher
SQLite3

-->Installation and Running
Using Python
Clone or download the project
Open terminal and navigate to project folder
Run the app:
python ice_cream_main.py

-->Using Docker
Build the Docker image:
docker build -t ice-cream-app .
Run the container:
docker run -it --rm ice-cream-app

-->How to Use
When the app starts, the menu appears with these options:
Browse Flavors
Search Flavors
View Cart
Register Customer
Suggest Flavor
View Ingredients
Add Allergen
View Allergens
Checkout
Exit

-->Test Steps
Start the app
Choose Browse Flavors and test seasonal filtering
Choose Search Flavors and try searching for "vanilla"
Add items to cart
View Cart and update or remove items
Register as a customer
Suggest a new flavor
View and add allergens
Checkout to complete the order
Exit and restart the app to confirm data is saved

-->Expected Results
All menu options should work
Cart calculations should be correct
Duplicate email registration should not work
Data should be saved in the database
Flavor suggestions and allergens should be stored

-->Database Structure
flavors
ingredients
customers
suggestions
allergens
These tables are created and managed using SQLite queries inside the code.

-->Files in the Project
ice_cream_main.py
requirements.txt
Dockerfile
README.md
ice_cream.db (created after first run)

-->Docker Information(Docker Commands)
To build and run using Docker:
docker build -t ice-cream-app .
docker run -it --rm ice-cream-app

-->Code Overview
All database operations are handled using SQLite queries
Functions are grouped by features: flavors, customers, allergens, cart
Code is written in Python using standard libraries only
