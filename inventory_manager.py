"""CPS 310 - Homework 1: Inventory Manager
Instructor solution checkpoint.
"""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


def display_menu():
    """Display the main Inventory Manager menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def load_inventory(filename):
    """Load inventory records from a pipe-delimited text file."""
    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                name, category, quantity = line.split("|")
                inventory.append(
                    {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                    }
                )
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save the complete inventory to a pipe-delimited text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|{item["quantity"]}\n'
            )


def view_inventory(inventory):
    """Display all inventory items in a numbered list."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")
    for index, item in enumerate(inventory, start=1):
        print(
            f'{index}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )


def validate_new_item(inventory, name, category, quantity):
    """Return an error message for invalid item data, or None if valid."""
    name = str(name).strip()
    category = str(category).strip()
    if not name:
        return "Item name cannot be empty."
    if "|" in name:
        return "Item name may not contain the | character."
    if any(item["name"].lower() == name.lower() for item in inventory):
        return "An item with that name already exists."
    if not category:
        return "Category cannot be empty."
    if "|" in category:
        return "Category may not contain the | character."
    if isinstance(quantity, bool) or not str(quantity).strip().isdigit():
        return "Quantity must be a nonnegative whole number."
    return None


def add_item_record(inventory, name, category, quantity):
    """Add a valid item and return True, or leave the list alone and return False."""
    if validate_new_item(inventory, name, category, quantity) is not None:
        return False
    inventory.append({"name": name.strip(), "category": category.strip(),
                      "quantity": int(str(quantity).strip())})
    return True


def remove_item_by_number(inventory, item_number):
    """Remove a 1-based item number and return its record, or None."""
    if not isinstance(item_number, int) or isinstance(item_number, bool):
        return None
    if item_number < 1 or item_number > len(inventory):
        return None
    return inventory.pop(item_number - 1)


def update_item_quantity(inventory, item_number, new_quantity):
    """Update a 1-based item only for a nonnegative integer quantity."""
    if not isinstance(item_number, int) or isinstance(item_number, bool):
        return False
    if not (1 <= item_number <= len(inventory)):
        return False
    if isinstance(new_quantity, bool) or not str(new_quantity).strip().isdigit():
        return False
    inventory[item_number - 1]["quantity"] = int(str(new_quantity).strip())
    return True


def find_matching_items(inventory, search_term):
    """Return case-insensitive name matches; an empty query matches nothing."""
    search_term = str(search_term).strip().lower()
    if not search_term:
        return []
    return [item for item in inventory if search_term in item["name"].lower()]


def calculate_summary(inventory):
    """Return inventory counts without printing (category keys are lower-case)."""
    categories = {}
    for item in inventory:
        key = item["category"].lower()
        categories[key] = categories.get(key, 0) + 1
    return {
        "unique_items": len(inventory),
        "total_quantity": sum(item["quantity"] for item in inventory),
        "low_stock_items": sum(item["quantity"] < LOW_STOCK_THRESHOLD for item in inventory),
        "category_counts": categories,
    }


def add_item(inventory):
    """Prompt for data and use the testable validation and add helpers."""
    name = input("Enter the item name: ").strip()
    if not name or "|" in name or any(item["name"].lower() == name.lower() for item in inventory):
        print(validate_new_item(inventory, name, "category", 0))
        return
    category = input("Enter the category: ").strip()
    if not category or "|" in category:
        print(validate_new_item(inventory, name, category, 0))
        return
    quantity = input("Enter the quantity: ").strip()
    error = validate_new_item(inventory, name, category, quantity)
    if error:
        print(error)
        return
    add_item_record(inventory, name, category, quantity)
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added successfully.")


def update_quantity(inventory):
    """Read selections and delegate the change to update_item_quantity."""
    if not inventory:
        print("No inventory items found.")
        return
    view_inventory(inventory)
    selection_text = input("Enter the item number to update: ").strip()
    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return
    selection = int(selection_text)
    if not 1 <= selection <= len(inventory):
        print("Item number is outside the available range.")
        return
    quantity_text = input("Enter the new quantity: ").strip()
    if not update_item_quantity(inventory, selection, quantity_text):
        print("Quantity must be a nonnegative whole number.")
        return
    save_inventory(inventory, INVENTORY_FILE)
    print(f'{inventory[selection - 1]["name"]} quantity updated to {inventory[selection - 1]["quantity"]}.')


def remove_item(inventory):
    """Read an item number and delegate removal to the testable helper."""
    if not inventory:
        print("No inventory items found.")
        return
    view_inventory(inventory)
    selection_text = input("Enter the item number to remove: ").strip()
    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return
    removed = remove_item_by_number(inventory, int(selection_text))
    if removed is None:
        print("Item number is outside the available range.")
        return
    save_inventory(inventory, INVENTORY_FILE)
    print(f'Item removed: {removed["name"]}')


def search_inventory(inventory):
    """Read a search string and show results from find_matching_items."""
    search_term = input("Enter part or all of an item name: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return
    matches = find_matching_items(inventory, search_term)
    if not matches:
        print("No inventory items matched your search.")
        return
    print("\nSearch Results:")
    for index, item in enumerate(matches, start=1):
        print(f'{index}. {item["name"]} | {item["category"]} | Quantity: {item["quantity"]}')


def display_summary(inventory):
    """Display the counts returned by the testable summary helper."""
    summary = calculate_summary(inventory)
    print("\nInventory Summary")
    print(f'Unique items: {summary["unique_items"]}')
    print(f'Total quantity: {summary["total_quantity"]}')
    print(f'Low-stock items: {summary["low_stock_items"]}')
    print("\nItems by category:")
    if not summary["category_counts"]:
        print("No categories found.")
        return
    for key, count in summary["category_counts"].items():
        label = next(item["category"] for item in inventory if item["category"].lower() == key)
        print(f"{label}: {count}")


def main():
    """Run the Inventory Manager menu loop."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
        elif choice == "3":
            update_quantity(inventory)
        elif choice == "4":
            remove_item(inventory)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a menu option from 1 through 7.")


if __name__ == "__main__":
    main()
