# Ice Cream Parlor Management System

A simple Python application for managing ice cream flavors, ingredients, and customers using SQLite database.

## Features

- Browse ice cream flavors by season
- Search flavors by name or description
- Shopping cart to add favorite products
- Customer registration with allergy information
- Suggest new flavors
- View ingredient inventory
- Add and view allergens
- Simple checkout process

## Requirements

- Python 3.6 or higher
- SQLite3 (included with Python)

## Setup and Installation

### Method 1: Run with Python

1. Download or clone the files
2. Make sure Python is installed:
   ```bash
   python --version
   ```
3. Run the application:
   ```bash
   python ice_cream_main.py
   ```

### Method 2: Run with Docker

1. Build the Docker image:
   ```bash
   docker build -t ice-cream-app .
   ```

2. Run the container:
   ```bash
   docker run -it --rm ice-cream-app
   ```

## How to Use

When you start the application, you'll see a menu with these options:

1. **Browse Flavors** - View all flavors or filter by season
2. **Search Flavors** - Search by flavor name or description
3. **View Cart** - See items in your cart, update quantities, or remove items
4. **Register Customer** - Sign up with name, email, and allergies
5. **Suggest Flavor** - Suggest new flavors (requires customer registration)
6. **View Ingredients** - See current ingredient inventory
7. **Add Allergen** - Add new allergens to the system
8. **View Allergens** - See all registered allergens
9. **Checkout** - Complete your purchase
0. **Exit** - Close the application

## Testing Steps

Follow these steps to test the application:

### Basic Functionality Test

1. **Start the application:**
   ```bash
   python ice_cream_main.py
   ```

2. **Test flavor browsing:**
   - Choose option 1 (Browse Flavors)
   - Try filtering by season (press 1, 2, 3, or 4)
   - Try viewing all flavors (press Enter)
   - Add a flavor to cart by entering its ID and quantity

3. **Test flavor search:**
   - Choose option 2 (Search Flavors)
   - Search for "vanilla" or "chocolate"
   - Add search result to cart

4. **Test cart functionality:**
   - Choose option 3 (View Cart)
   - Check that items are displayed correctly
   - Try updating quantity (option 1)
   - Try removing an item (option 2)
   - Verify total calculation is correct

5. **Test customer registration:**
   - Choose option 4 (Register Customer)
   - Enter name: "John Smith"
   - Enter email: "john@test.com"
   - Enter allergies: "nuts, dairy" (or leave empty)
   - Try registering same email again (should fail)

6. **Test flavor suggestions:**
   - Choose option 5 (Suggest Flavor)
   - Should work only after registering as customer
   - Suggest: "Cookies and Cream" with description

7. **Test ingredient viewing:**
   - Choose option 6 (View Ingredients)
   - Verify ingredients are displayed with quantities and allergen info

8. **Test allergen management:**
   - Choose option 8 (View Allergens) to see current list
   - Choose option 7 (Add Allergen)
   - Add new allergen: "Soy" with description "Soy products"
   - Check it appears in allergen list

9. **Test checkout:**
   - Make sure cart has items
   - Choose option 9 (Checkout)
   - Confirm purchase with 'y'
   - Verify cart is cleared

10. **Test data persistence:**
    - Exit application (option 0)
    - Restart application
    - Check that customer data still exists
    - Database file "ice_cream.db" should be created in same folder

### Expected Results

- All menu options should work without errors
- Cart calculations should be accurate
- Search should return correct flavors
- Customer registration should prevent duplicate emails
- Data should persist after restarting application
- Database file should be created automatically

## Database Structure

The application creates these tables automatically:

- **flavors** - stores ice cream flavors with season and price info
- **ingredients** - tracks ingredient inventory and allergen status
- **customers** - customer information including allergies
- **suggestions** - customer flavor suggestions
- **allergens** - list of allergens with descriptions

## Files

- `ice_cream_main.py` - Main application file
- `README.md` - This documentation file
- `requirements.txt` - Python dependencies (minimal)
- `Dockerfile` - Docker configuration
- `ice_cream.db` - SQLite database (created automatically)

## Troubleshooting

**"No module named sqlite3"**
- SQLite3 comes with Python, try reinstalling Python

**"Permission denied" errors**
- Make sure you can write files in the current directory

**Application won't start**
- Check Python version is 3.6 or higher
- Make sure all files are in same directory

**Database errors**
- Delete "ice_cream.db" file and restart to reset database