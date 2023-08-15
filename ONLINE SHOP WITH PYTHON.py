import sqlite3
import getpass

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append((product, quantity))

    def calculate_total(self):
        total = 0
        for product, quantity in self.items:
            total += product.price * quantity
        return total

    def checkout(self):
        total = self.calculate_total()
        print("Total price: ${:.2f}".format(total))
        while True:
            payment = input("Enter payment amount: $")
            if payment.replace('.', '').isdigit():
                payment = float(payment)
                if payment >= total:
                    change = payment - total
                    print("Thank you for your purchase!")
                    print("Your change: ${:.2f}".format(change))
                    self.items = []  # Empty the cart after successful checkout
                    break
                else:
                    print("Insufficient payment. Please enter a higher amount.")
            else:
                print("Invalid input. Please enter a valid amount.")

def create_user(username, password):
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print("User created successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

def login(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful.")
        return True
    else:
        print("Login failed. Invalid credentials.")
        return False

def logout():
    print("Logout successful.")

def main():
    # Connect to or create a database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()

    products = [
        Product("Item 1", 10.99),
        Product("Item 2", 5.49),
        Product("Item 3", 7.25)
    ]

    cart = ShoppingCart()

    while True:
        print("1. Login")
        print("2. Create User")
        print("3. Shop")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            if login(username, password):
                while True:
                    print("Available products:")
                    for i, product in enumerate(products, start=1):
                        print("{}. {} - ${:.2f}".format(i, product.name, product.price))
                    
                    product_choice = input("Select a product (1-{}), or 'q' to quit shopping: ".format(len(products)))
                    
                    if product_choice == 'q':
                        break
                    
                    if product_choice.isdigit():
                        product_choice = int(product_choice)
                        if 1 <= product_choice <= len(products):
                            selected_product = products[product_choice - 1]
                            quantity = int(input("Enter quantity: "))
                            cart.add_item(selected_product, quantity)
                        else:
                            print("Invalid choice. Please select a valid product.")
                    else:
                        print("Invalid input. Please enter a valid choice.")

                cart.checkout()
                while True:
                    action = input("Logout (y/n): ").lower()
                    if action == 'y':
                        logout()
                        break
        elif choice == '2':
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            create_user(username, password)
        elif choice == '3':
            print("You need to log in first.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

    conn.close()

if __name__ == "__main__":
    main()
