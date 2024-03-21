import tkinter as tk
from tkinter import messagebox

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Check if username and password match
    if username == "admin" and password == "password":
        # Destroy login window
        login_window.destroy()
        # Open product selection window
        open_product_selection_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def open_product_selection_window():
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

# Create login window
login_window = tk.Tk()
login_window.title("Login")

# Username label and entry
username_label = tk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)

username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Password label and entry
password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)

password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, columnspan=2, padx=5, pady=5)

login_window.mainloop()
