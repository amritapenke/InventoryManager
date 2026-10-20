# Inventory Manager

A command-line Python application by Amrita Penke for CPS 310.
It tracks campus supplies using a list of dictionaries and a text file.

## Features
- View numbered inventory items.
- Add items with name, category, and quantity validation.
- Reject duplicate names regardless of capitalization.
- Update quantities and remove items.
- Search item names using case-insensitive partial matches.
- Summarize unique items, total quantity, low stock, and categories.
- Save changes between program sessions.
- Start with an empty inventory if the data file is missing.

## Requirements
Python 3. No external packages are required.

## Project Files
- inventory_manager.py: application code.
- inventory.txt: saved inventory records.
- README.md: setup and usage instructions.
- TESTING.md: test procedures and observed results.
- AI_USAGE.md: disclosure of AI assistance and verification.
- .gitignore: excludes environments, caches, and sensitive files.

## Data Format
Each line contains Name|Category|Quantity:

    Laptop Charger|Electronics|12

Quantities are nonnegative integers. Names and categories cannot
contain the pipe character. Item names must be unique regardless
of capitalization.

## Running on macOS
Open a terminal in the InventoryManager folder and run:

    python3 inventory_manager.py

## Menu
1. View inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit

## Sample Interaction
    Choose an option: 3
    Enter the item number to update: 1
    Enter the new quantity: 12
    Laptop Charger quantity updated to 12.

## Testing
See TESTING.md for test inputs, expected behavior, observed results,
and pass/fail status. Tests cover normal operations, invalid input,
missing files, searches, summary calculations, and persistence.

## Git and GitHub Development
The application was developed incrementally with focused commits.
Search was developed on feature/inventory-search after issue #1
was created, then merged into main through pull request #2
using a merge commit.

## Known Limitations
- Existing data files must follow the required three-field format.
- File permission errors are not handled.
- The program supports one user at a time.
- Invalid input returns to the menu instead of repeating the prompt.
- Category names appear in lowercase in the summary.

## Future Improvements
- Add sorting and filtering.
- Handle malformed data and file permission errors.
- Add automated regression tests.
- Support exporting inventory reports.