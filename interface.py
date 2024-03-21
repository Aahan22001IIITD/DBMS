import tkinter as tk
from tkinter import messagebox

# Sample user data
users_data = [
    (700, 'kartikeya', 'example@gmail.com', '1234', 'Dilshad Garden', '8888888888', 300, 800),
    (701, 'Aarav', 'aarav@example.com', 'pass123', 'Green Park', '7777777777', 301, 801),
    (702, 'Bhavna', 'bhavna@example.net', 'abcd1234', 'Lajpat Nagar', '6666666666', 302, 802),
    (703, 'Chetan', 'chetan@example.org', 'xyz789', 'Rohini', '5555555555', 303, 803),
    (704, 'Divya', 'divya@example.com', 'div123', 'Pitampura', '4444444444', 304, 804),
    (705, 'Esha', 'esha@example.net', 'esha456', 'Janakpuri', '3333333333', 305, 805),
    (706, 'Farhan', 'farhan@example.org', 'far789', 'Vasant Kunj', '2222222222', 306, 806),
    (707, 'Gauri', 'gauri@example.com', 'gauri123', 'Saket', '1111111111', 307, 807),
    (708, 'Himanshu', 'himanshu@example.net', 'himan456', 'Dwarka', '9999999999', 308, 808),
    (709, 'Isha', 'isha@example.org', 'isha789', 'Mayur Vihar', '8888888888', 309, 809)
]

def login():
    email_id = email_id_entry.get()
    password = password_entry.get()
    
    # Check if email_id and password match with any user's credentials
    for user_data in users_data:
        if email_id == user_data[2] and password == user_data[3]:
            # Destroy login window
            login_window.destroy()
            # Open product selection window
            open_product_selection_window(user_data)
            return
    # If no match found, show error message
    messagebox.showerror("Error", "Invalid email Id or password")

def open_product_selection_window(user_data):
    # Create new window for product selection
    product_window = tk.Tk()
    product_window.title("Product Selection")
    
    def add_to_cart():
        selected_item = products_listbox.get(tk.ACTIVE)
        cart_listbox.insert(tk.END, selected_item)
    
    # Products listbox
    products_label = tk.Label(product_window, text="Products:")
    products_label.grid(row=0, column=0, padx=5, pady=5)

    products = ["Apples", "Bananas", "Oranges", "Bread", "Milk", "Eggs", "Cheese"]
    products_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    for product in products:
        products_listbox.insert(tk.END, product)
    products_listbox.grid(row=1, column=0, padx=5, pady=5)

    # Add to Cart button
    add_button = tk.Button(product_window, text="Add to Cart", command=add_to_cart)
    add_button.grid(row=2, column=0, padx=5, pady=5)

    # Cart listbox
    cart_label = tk.Label(product_window, text="Cart:")
    cart_label.grid(row=0, column=1, padx=5, pady=5)

    cart_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    cart_listbox.grid(row=1, column=1, padx=5, pady=5)

    product_window.mainloop()

def register():
    # Create a registration window
    register_window = tk.Tk()
    register_window.title("Register")

    # Add registration fields
    tk.Label(register_window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(register_window).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(register_window, text="Email ID:").grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(register_window).grid(row=1, column=1, padx=5, pady=5)
    tk.Label(register_window, text="Password:").grid(row=2, column=0, padx=5, pady=5)
    tk.Entry(register_window, show="*").grid(row=2, column=1, padx=5, pady=5)
    tk.Label(register_window, text="Address:").grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(register_window).grid(row=3, column=1, padx=5, pady=5)
    tk.Label(register_window, text="Mobile Number:").grid(row=4, column=0, padx=5, pady=5)
    tk.Entry(register_window).grid(row=4, column=1, padx=5, pady=5)

    # Register button
    tk.Button(register_window, text="Register").grid(row=5, columnspan=2, padx=5, pady=5)

    # Back button
    def go_back():
        register_window.destroy()

    tk.Button(register_window, text="Back", command=go_back).grid(row=6, columnspan=2, padx=5, pady=5)

    register_window.mainloop()

def run():
# Create login window
    login_window = tk.Tk()
    login_window.title("Login")

    # Username label and entry
    tk.Label(login_window, text="Email ID:").grid(row=0, column=0, padx=5, pady=5)
    email_id_entry = tk.Entry(login_window)
    email_id_entry.grid(row=0, column=1, padx=5, pady=5)

    # Password label and entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Login button
    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, padx=5, pady=5)

    # Register button
    tk.Button(login_window, text="Register", command=register).grid(row=3, columnspan=2, padx=5, pady=5)

    login_window.mainloop()
