import sqlite3
import json
from datetime import datetime

class IceCreamDB:
    def __init__(self, db_name="ice_cream.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.setup_db()
        self.add_sample_data()
    
    def setup_db(self):
        c = self.conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS flavors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            season TEXT,
            price REAL,
            available INTEGER DEFAULT 1
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            qty INTEGER,
            unit TEXT,
            allergen INTEGER DEFAULT 0
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            allergies TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            flavor_name TEXT,
            description TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS allergens (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            description TEXT
        )''')
        
        self.conn.commit()
    
    def add_sample_data(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM flavors")
        if c.fetchone()[0] > 0:
            return
        
        flavors = [
            ("Vanilla", "Basic vanilla flavor", "summer", 4.50),
            ("Chocolate", "Rich chocolate", "winter", 5.00),
            ("Strawberry", "Fresh strawberry", "spring", 4.75),
            ("Mint", "Cool mint", "summer", 4.90)
        ]
        
        c.executemany("INSERT INTO flavors (name, description, season, price) VALUES (?, ?, ?, ?)", flavors)
        
        ingredients = [
            ("Milk", 50, "liters", 1),
            ("Sugar", 25, "kg", 0),
            ("Vanilla", 5, "bottles", 0),
            ("Chocolate", 15, "kg", 0)
        ]
        
        c.executemany("INSERT INTO ingredients (name, qty, unit, allergen) VALUES (?, ?, ?, ?)", ingredients)
        
        allergens = [
            ("Dairy", "Milk products"),
            ("Nuts", "Tree nuts"),
            ("Eggs", "Egg products")
        ]
        
        c.executemany("INSERT INTO allergens (name, description) VALUES (?, ?)", allergens)
        
        self.conn.commit()
    
    def get_flavors(self, season=None, search=None):
        c = self.conn.cursor()
        query = "SELECT * FROM flavors WHERE available = 1"
        params = []
        
        if season:
            query += " AND season = ?"
            params.append(season)
        
        if search:
            query += " AND (name LIKE ? OR description LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        c.execute(query, params)
        return [dict(row) for row in c.fetchall()]
    
    def get_ingredients(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM ingredients")
        return [dict(row) for row in c.fetchall()]
    
    def add_customer(self, name, email, allergies):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO customers (name, email, allergies) VALUES (?, ?, ?)", 
                     (name, email, json.dumps(allergies)))
            self.conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def add_suggestion(self, customer_id, flavor, desc):
        c = self.conn.cursor()
        c.execute("INSERT INTO suggestions (customer_id, flavor_name, description) VALUES (?, ?, ?)", 
                 (customer_id, flavor, desc))
        self.conn.commit()
        return c.lastrowid
    
    def add_allergen(self, name, desc=""):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO allergens (name, description) VALUES (?, ?)", (name, desc))
            self.conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            c.execute("SELECT id FROM allergens WHERE name = ?", (name,))
            return c.fetchone()[0]
    
    def get_allergens(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM allergens")
        return [dict(row) for row in c.fetchall()]

class Cart:
    def __init__(self):
        self.items = []
    
    def add_item(self, flavor_id, name, qty, price):
        for item in self.items:
            if item['id'] == flavor_id:
                item['qty'] += qty
                return
        
        self.items.append({
            'id': flavor_id,
            'name': name,
            'qty': qty,
            'price': price
        })
    
    def remove_item(self, flavor_id):
        self.items = [item for item in self.items if item['id'] != flavor_id]
    
    def update_qty(self, flavor_id, qty):
        for item in self.items:
            if item['id'] == flavor_id:
                if qty <= 0:
                    self.remove_item(flavor_id)
                else:
                    item['qty'] = qty
                break
    
    def get_total(self):
        return sum(item['price'] * item['qty'] for item in self.items)
    
    def clear(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0

class IceCreamApp:
    def __init__(self):
        self.db = IceCreamDB()
        self.cart = Cart()
        self.current_customer = None
    
    def show_menu(self):
        print("\n" + "="*40)
        print("ICE CREAM PARLOR")
        print("="*40)
        print("1. Browse Flavors")
        print("2. Search Flavors") 
        print("3. View Cart")
        print("4. Register Customer")
        print("5. Suggest Flavor")
        print("6. View Ingredients")
        print("7. Add Allergen")
        print("8. View Allergens")
        print("9. Checkout")
        print("0. Exit")
        print("="*40)
    
    def browse_flavors(self):
        print("\nBROWSE FLAVORS")
        print("1. Spring  2. Summer  3. Fall  4. Winter")
        
        choice = input("Filter by season (1-4) or Enter for all: ").strip()
        seasons = {"1": "spring", "2": "summer", "3": "fall", "4": "winter"}
        season = seasons.get(choice)
        
        flavors = self.db.get_flavors(season=season)
        
        if not flavors:
            print("No flavors found")
            return
        
        print(f"\n{'ID':<5} {'Name':<15} {'Season':<10} {'Price':<8} {'Description'}")
        print("-" * 60)
        
        for f in flavors:
            print(f"{f['id']:<5} {f['name']:<15} {f['season']:<10} ${f['price']:<7.2f} {f['description']}")
        
        self.select_flavor(flavors)
    
    def search_flavors(self):
        search = input("\nEnter search term: ").strip()
        
        if not search:
            print("Enter a search term")
            return
        
        flavors = self.db.get_flavors(search=search)
        
        if not flavors:
            print(f"No flavors found for '{search}'")
            return
        
        print(f"\nSearch results for '{search}':")
        print(f"{'ID':<5} {'Name':<15} {'Season':<10} {'Price':<8} {'Description'}")
        print("-" * 60)
        
        for f in flavors:
            print(f"{f['id']:<5} {f['name']:<15} {f['season']:<10} ${f['price']:<7.2f} {f['description']}")
        
        self.select_flavor(flavors)
    
    def select_flavor(self, flavors):
        try:
            flavor_id = int(input("\nEnter flavor ID to add to cart (0 to go back): "))
            
            if flavor_id == 0:
                return
            
            flavor = next((f for f in flavors if f['id'] == flavor_id), None)
            
            if not flavor:
                print("Invalid flavor ID")
                return
            
            qty = int(input("Enter quantity: "))
            
            if qty <= 0:
                print("Quantity must be greater than 0")
                return
            
            self.cart.add_item(flavor['id'], flavor['name'], qty, flavor['price'])
            print(f"Added {qty} x {flavor['name']} to cart")
            
        except ValueError:
            print("Enter valid numbers")
    
    def view_cart(self):
        print("\nYOUR CART")
        
        if self.cart.is_empty():
            print("Cart is empty")
            return
        
        print(f"{'Flavor':<20} {'Qty':<5} {'Price':<8} {'Total'}")
        print("-" * 40)
        
        for item in self.cart.items:
            total = item['price'] * item['qty']
            print(f"{item['name']:<20} {item['qty']:<5} ${item['price']:<7.2f} ${total:.2f}")
        
        print("-" * 40)
        print(f"{'TOTAL':<33} ${self.cart.get_total():.2f}")
        
        print("\n1. Update quantity  2. Remove item  3. Clear cart  4. Back")
        
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            self.update_cart()
        elif choice == "2":
            self.remove_from_cart()
        elif choice == "3":
            self.cart.clear()
            print("Cart cleared")
    
    def update_cart(self):
        try:
            flavor_id = int(input("Enter flavor ID: "))
            qty = int(input("Enter new quantity (0 to remove): "))
            self.cart.update_qty(flavor_id, qty)
            print("Cart updated")
        except ValueError:
            print("Enter valid numbers")
    
    def remove_from_cart(self):
        try:
            flavor_id = int(input("Enter flavor ID to remove: "))
            self.cart.remove_item(flavor_id)
            print("Item removed")
        except ValueError:
            print("Enter valid flavor ID")
    
    def register_customer(self):
        print("\nCUSTOMER REGISTRATION")
        
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        
        if not name or not email:
            print("Name and email required")
            return
        
        allergies_input = input("Allergies (comma separated, or Enter to skip): ").strip()
        allergies = [a.strip() for a in allergies_input.split(",")] if allergies_input else []
        
        customer_id = self.db.add_customer(name, email, allergies)
        
        if customer_id:
            self.current_customer = {
                'id': customer_id,
                'name': name,
                'email': email,
                'allergies': allergies
            }
            print(f"Customer registered! ID: {customer_id}")
        else:
            print("Email already exists")
    
    def suggest_flavor(self):
        if not self.current_customer:
            print("Please register first")
            return
        
        print("\nSUGGEST FLAVOR")
        
        name = input("Flavor name: ").strip()
        desc = input("Description: ").strip()
        
        if not name:
            print("Flavor name required")
            return
        
        suggestion_id = self.db.add_suggestion(self.current_customer['id'], name, desc)
        print(f"Suggestion submitted! ID: {suggestion_id}")
    
    def view_ingredients(self):
        print("\nINGREDIENTS")
        
        ingredients = self.db.get_ingredients()
        
        print(f"{'Name':<15} {'Qty':<8} {'Unit':<8} {'Allergen'}")
        print("-" * 40)
        
        for ing in ingredients:
            allergen = "Yes" if ing['allergen'] else "No"
            print(f"{ing['name']:<15} {ing['qty']:<8} {ing['unit']:<8} {allergen}")
    
    def add_allergen(self):
        print("\nADD ALLERGEN")
        
        name = input("Allergen name: ").strip()
        
        if not name:
            print("Name required")
            return
        
        desc = input("Description: ").strip()
        
        allergen_id = self.db.add_allergen(name, desc)
        print(f"Allergen added! ID: {allergen_id}")
    
    def view_allergens(self):
        print("\nALLERGENS")
        
        allergens = self.db.get_allergens()
        
        print(f"{'ID':<5} {'Name':<15} {'Description'}")
        print("-" * 35)
        
        for a in allergens:
            print(f"{a['id']:<5} {a['name']:<15} {a['description']}")
    
    def checkout(self):
        if self.cart.is_empty():
            print("Cart is empty")
            return
        
        print("\nCHECKOUT")
        print(f"Total: ${self.cart.get_total():.2f}")
        
        confirm = input("Confirm purchase? (y/n): ").strip().lower()
        
        if confirm == 'y':
            print("Order confirmed! Thank you!")
            self.cart.clear()
        else:
            print("Purchase cancelled")
    
    def run(self):
        print("Welcome to Ice Cream Parlor!")
        
        while True:
            try:
                self.show_menu()
                choice = input("\nEnter choice: ").strip()
                
                if choice == "0":
                    print("Thank you!")
                    break
                elif choice == "1":
                    self.browse_flavors()
                elif choice == "2":
                    self.search_flavors()
                elif choice == "3":
                    self.view_cart()
                elif choice == "4":
                    self.register_customer()
                elif choice == "5":
                    self.suggest_flavor()
                elif choice == "6":
                    self.view_ingredients()
                elif choice == "7":
                    self.add_allergen()
                elif choice == "8":
                    self.view_allergens()
                elif choice == "9":
                    self.checkout()
                else:
                    print("Invalid choice")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    app = IceCreamApp()
    app.run()
