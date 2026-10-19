"""Inventory Manager: track campus supplies.

Author: Amrita Penke
Course: CPS 310
"""

INVENTORY_FILE = "inventory.txt"


def load_inventory(filename):
    """Load inventory records, returning an empty list if the file is missing."""
    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    name, category, quantity = line.strip().split("|")
                    inventory.append({
                        "name": name,
                        "category": category,
                        "quantity": int(quantity)
                    })
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save the complete inventory using pipe-separated records."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f"{item['name']}|{item['category']}|{item['quantity']}\n"
            )


def display_menu():
    """Display the inventory menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def view_inventory(inventory):
    """Display inventory items with numbering starting at one."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")
    for number, item in enumerate(inventory, start=1):
        print(
            f"{number}. {item['name']} | {item['category']} | "
            f"Quantity: {item['quantity']}"
        )

def add_item(inventory):
    """Validate and add an item, returning True when successful."""
    name = input("Enter the item name: ").strip()

    if not name or "|" in name:
        print("Item name cannot be empty or contain |.")
        return False

    for item in inventory:
        if item["name"].casefold() == name.casefold():
            print("An item with that name already exists.")
            return False

    category = input("Enter the category: ").strip()

    if not category or "|" in category:
        print("Category cannot be empty or contain |.")
        return False

    quantity_text = input("Enter the quantity: ").strip()

    try:
        quantity = int(quantity_text)
    except ValueError:
        print("Quantity must be a nonnegative whole number.")
        return False

    if quantity < 0:
        print("Quantity must be a nonnegative whole number.")
        return False

    inventory.append({
        "name": name,
        "category": category,
        "quantity": quantity
    })
    print("Item added successfully.")
    return True

def main():
    """Load inventory and handle the available menu choices."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            if add_item(inventory):
                save_inventory(inventory, INVENTORY_FILE)
        elif choice == "7":
            print("Goodbye!")
            break
        elif choice in ["3", "4", "5", "6"]:
            print("This feature is not available yet.")
        else:
            print("Please enter a number from 1 through 7.")


if __name__ == "__main__":
    main()         