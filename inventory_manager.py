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