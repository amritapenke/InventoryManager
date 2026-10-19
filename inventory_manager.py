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


def main():
    """Load inventory and handle the available menu choices."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_inventory(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        elif choice in ["2", "3", "4", "5", "6"]:
            print("This feature is not available yet.")
        else:
            print("Please enter a number from 1 through 7.")


if __name__ == "__main__":
    main()         