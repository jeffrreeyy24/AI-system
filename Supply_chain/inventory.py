import tkinter as tk
from tkinter import ttk

inventory = [
    {"product_name": "Egg", "stock": 50, "reorder_point": 30, "reorder_quantity": 0},
    {"product_name": "Milk", "stock": 20, "reorder_point": 25, "reorder_quantity": 0},
    {"product_name": "Rice", "stock": 10, "reorder_point": 15, "reorder_quantity": 0}
]

def calculate_reorder():
    for item in inventory:
        if item["stock"] <= item["reorder_point"]:
            item["reorder_quantity"] = item["reorder_point"] - item["stock"] + 10  # Add safety stock
        else:
            item["reorder_quantity"] = 0
    update_table()

def update_table():
    table.delete(*table.get_children())  # Clear the table
    for i, item in enumerate(inventory):
        table.insert("", "end", iid=f"I{i}",
                     values=(item["product_name"], item["stock"], item["reorder_point"], item["reorder_quantity"]))


# Function to update stock levels and automatically adjust reorder quantity
def update_stock():
    selected_item = table.selection()
    if not selected_item:
        return

    index = int(selected_item[0][1:])
    try:
        new_stock = int(stock_update_entry.get())
        inventory[index]["stock"] = new_stock

        # Automatically adjust reorder quantity based on updated stock
        if inventory[index]["stock"] <= inventory[index]["reorder_point"]:
            inventory[index]["reorder_quantity"] = inventory[index]["reorder_point"] - inventory[index]["stock"] + 10  # Add safety stock
        else:
            inventory[index]["reorder_quantity"] = 0

        update_table()
        stock_update_entry.delete(0, tk.END)
    except ValueError:
        print("Please enter a valid stock quantity.")


# Function to add a new inventory item
def add_item():
    try:
        product_name = product_name_entry.get()
        stock = int(stock_entry.get())
        reorder_point = int(reorder_point_entry.get())

        if not product_name:
            print("Product name cannot be empty.")
            return

        new_item = {
            "product_name": product_name,
            "stock": stock,
            "reorder_point": reorder_point,
            "reorder_quantity": 0
        }
        inventory.append(new_item)
        update_table()

        # Clear input fields
        product_name_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)
        reorder_point_entry.delete(0, tk.END)
    except ValueError:
        print("Please enter valid numeric values for stock and reorder point.")

root = tk.Tk()
root.title("Inventory Management")

# Table for inventory display
table = ttk.Treeview(root, columns=("Product Name", "Stock", "Reorder Point", "Reorder Quantity"), show="headings")
table.heading("Product Name", text="Product Name")
table.heading("Stock", text="Stock")
table.heading("Reorder Point", text="Reorder Point")
table.heading("Reorder Quantity", text="Reorder Quantity")
table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Input fields for adding a new item
add_frame = tk.LabelFrame(root, text="Add New Product", padx=10, pady=10)
add_frame.pack(fill=tk.X, padx=10, pady=10)

tk.Label(add_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
product_name_entry = tk.Entry(add_frame, width=15)
product_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Stock:").grid(row=0, column=2, padx=5, pady=5)
stock_entry = tk.Entry(add_frame, width=10)
stock_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(add_frame, text="Reorder Point:").grid(row=0, column=4, padx=5, pady=5)
reorder_point_entry = tk.Entry(add_frame, width=10)
reorder_point_entry.grid(row=0, column=5, padx=5, pady=5)

add_button = tk.Button(add_frame, text="Add Item", command=add_item)
add_button.grid(row=0, column=6, padx=10, pady=5)

# Stock update frame
update_frame = tk.LabelFrame(root, text="Update Stock", padx=10, pady=10)
update_frame.pack(fill=tk.X, padx=10, pady=10)

tk.Label(update_frame, text="New Stock:").grid(row=0, column=0, padx=5, pady=5)
stock_update_entry = tk.Entry(update_frame, width=10)
stock_update_entry.grid(row=0, column=1, padx=5, pady=5)

update_button = tk.Button(update_frame, text="Update Stock", command=update_stock)
update_button.grid(row=0, column=2, padx=10, pady=5)

calculate_reorder()

# Run the application
root.mainloop()
