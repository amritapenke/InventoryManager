"""Automated regression tests for the Homework 2 Inventory Manager."""

import copy
import pytest

from inventory_manager import (
    load_inventory, save_inventory, find_matching_items,
    remove_item_by_number, update_item_quantity,
    validate_new_item, add_item_record, calculate_summary,
)


@pytest.fixture
def sample_inventory():
    """Fresh independent copy on every test (multiple categories and low stock)."""
    return [
        {"name": "Laptop Charger", "category": "Electronics", "quantity": 8},
        {"name": "Printer Paper", "category": "Office Supplies", "quantity": 25},
        {"name": "USB-C Cable", "category": "electronics", "quantity": 4},
        {"name": "Sticky Notes", "category": "Office Supplies", "quantity": 3},
    ]


# File input/output: every file test uses tmp_path, never real inventory.txt.
def test_load_valid_inventory_and_integer_quantities(tmp_path):
    # Arrange
    file = tmp_path / "inventory.txt"
    file.write_text("Pen|Office|2\nMouse|Electronics|10\n", encoding="utf-8")
    # Act
    result = load_inventory(file)
    # Assert
    assert result == [{"name": "Pen", "category": "Office", "quantity": 2},
                      {"name": "Mouse", "category": "Electronics", "quantity": 10}]
    assert type(result[0]["quantity"]) is int


def test_load_ignores_blank_lines(tmp_path):
    # Arrange
    file = tmp_path / "inventory.txt"
    file.write_text("\nPen|Office|2\n\n  \n", encoding="utf-8")
    # Act
    result = load_inventory(file)
    # Assert
    assert result == [{"name": "Pen", "category": "Office", "quantity": 2}]


def test_load_missing_file_returns_empty_list(tmp_path):
    # Arrange
    missing = tmp_path / "does_not_exist.txt"
    # Act
    result = load_inventory(missing)
    # Assert
    assert result == []


def test_save_multiple_items_uses_pipe_format(tmp_path, sample_inventory):
    # Arrange
    file = tmp_path / "saved.txt"
    # Act
    save_inventory(sample_inventory, file)
    # Assert
    assert file.read_text(encoding="utf-8") == (
        "Laptop Charger|Electronics|8\nPrinter Paper|Office Supplies|25\n"
        "USB-C Cable|electronics|4\nSticky Notes|Office Supplies|3\n"
    )


def test_save_empty_inventory_creates_empty_file(tmp_path):
    # Arrange
    file = tmp_path / "empty.txt"
    # Act
    save_inventory([], file)
    # Assert
    assert file.exists()
    assert file.read_text(encoding="utf-8") == ""


def test_save_load_round_trip(tmp_path, sample_inventory):
    # Arrange
    file = tmp_path / "round_trip.txt"
    expected = copy.deepcopy(sample_inventory)
    # Act
    save_inventory(sample_inventory, file)
    reloaded = load_inventory(file)
    # Assert
    assert reloaded == expected


# Search
@pytest.mark.parametrize(
    "term,expected_names",
    [
        ("Laptop Charger", ["Laptop Charger"]),
        ("charger", ["Laptop Charger"]),
        ("LAPTOP", ["Laptop Charger"]),
        ("xyz", []),
        ("", []),
        ("   ", []),
    ],
    ids=["exact", "partial", "case_insensitive", "no_match", "empty", "whitespace"],
)
def test_search_known_terms(sample_inventory, term, expected_names):
    # Arrange: sample_inventory fixture
    # Act
    matches = find_matching_items(sample_inventory, term)
    # Assert
    assert [item["name"] for item in matches] == expected_names


def test_search_returns_multiple_matches(sample_inventory):
    # Arrange: fixture contains two items matching 'paper' and 'notes'? Add shared prefix.
    sample_inventory.append({"name": "Laptop Sleeve", "category": "Electronics", "quantity": 7})
    # Act
    result = find_matching_items(sample_inventory, "lap")
    # Assert
    assert [item["name"] for item in result] == ["Laptop Charger", "Laptop Sleeve"]


# Removal
@pytest.mark.parametrize(
    "number,expected_name,remaining",
    [(1, "Laptop Charger", ["Printer Paper", "USB-C Cable", "Sticky Notes"]),
     (2, "Printer Paper", ["Laptop Charger", "USB-C Cable", "Sticky Notes"]),
     (4, "Sticky Notes", ["Laptop Charger", "Printer Paper", "USB-C Cable"])],
    ids=["first", "middle", "last"],
)
def test_remove_valid_positions(sample_inventory, number, expected_name, remaining):
    # Arrange: fixture
    # Act
    removed = remove_item_by_number(sample_inventory, number)
    # Assert
    assert removed["name"] == expected_name
    assert [item["name"] for item in sample_inventory] == remaining


@pytest.mark.parametrize("number", [0, -1, 5, 100], ids=["zero", "negative", "too_large", "far_too_large"])
def test_remove_invalid_numbers_preserves_list(sample_inventory, number):
    # Arrange
    expected = copy.deepcopy(sample_inventory)
    # Act
    removed = remove_item_by_number(sample_inventory, number)
    # Assert
    assert removed is None
    assert sample_inventory == expected


def test_remove_from_empty_inventory():
    # Arrange
    inventory = []
    # Act
    removed = remove_item_by_number(inventory, 1)
    # Assert
    assert removed is None and inventory == []


# Update

def test_update_quantity_changes_only_selected_item(sample_inventory):
    # Arrange
    expected_other = copy.deepcopy(sample_inventory[0])
    # Act
    success = update_item_quantity(sample_inventory, 2, 11)
    # Assert
    assert success is True
    assert sample_inventory[1]["quantity"] == 11
    assert sample_inventory[0] == expected_other
    assert sample_inventory[2]["quantity"] == 4


def test_update_quantity_accepts_zero(sample_inventory):
    # Arrange: fixture
    # Act
    success = update_item_quantity(sample_inventory, 1, 0)
    # Assert
    assert success is True
    assert sample_inventory[0]["quantity"] == 0


@pytest.mark.parametrize("number,quantity", [(0, 2), (-1, 2), (5, 2), (1, -1), (1, "abc")],
                         ids=["zero_number", "negative_number", "oversized_number", "negative_quantity", "nonnumeric_quantity"])
def test_update_invalid_input_preserves_list(sample_inventory, number, quantity):
    # Arrange
    before = copy.deepcopy(sample_inventory)
    # Act
    result = update_item_quantity(sample_inventory, number, quantity)
    # Assert
    assert result is False
    assert sample_inventory == before


# Add-item validation
@pytest.mark.parametrize(
    "name,category,quantity,valid",
    [("HDMI Cable", "Electronics", 6, True),
     ("", "Office", 2, False),
     ("  ", "Office", 2, False),
     ("Thing", "", 2, False),
     ("Thing", "  ", 2, False),
     ("Bad|Name", "Office", 2, False),
     ("Thing", "Bad|Category", 2, False),
     ("Thing", "Office", -1, False),
     ("Laptop Charger", "Office", 2, False),
     ("lApToP cHaRgEr", "Office", 2, False),
     ("Thing", "Office", "six", False),
     ("Thing", "Office", 0, True)],
    ids=["valid", "empty_name", "blank_name", "empty_category", "blank_category",
         "pipe_in_name", "pipe_in_category", "negative_quantity", "duplicate_name",
         "duplicate_case_insensitive", "nonnumeric_quantity", "zero_quantity"],
)
def test_validate_new_item_rules(sample_inventory, name, category, quantity, valid):
    # Arrange: sample_inventory fixture
    # Act
    error = validate_new_item(sample_inventory, name, category, quantity)
    # Assert
    assert (error is None) is valid


def test_add_valid_item_appends_record(sample_inventory):
    # Arrange
    count = len(sample_inventory)
    # Act
    result = add_item_record(sample_inventory, "HDMI Cable", "Electronics", "6")
    # Assert
    assert result is True
    assert len(sample_inventory) == count + 1
    assert sample_inventory[-1] == {"name": "HDMI Cable", "category": "Electronics", "quantity": 6}


def test_add_invalid_item_preserves_inventory(sample_inventory):
    # Arrange
    before = copy.deepcopy(sample_inventory)
    # Act
    result = add_item_record(sample_inventory, "LAPTOP CHARGER", "Electronics", 2)
    # Assert
    assert result is False
    assert sample_inventory == before


# Summary
def test_summary_counts_all_items_and_quantities(sample_inventory):
    # Arrange: fixture has 4 items: 8, 25, 4, 3
    # Act
    result = calculate_summary(sample_inventory)
    # Assert
    assert result["unique_items"] == 4
    assert result["total_quantity"] == 40
    assert result["low_stock_items"] == 2


def test_summary_groups_categories_ignoring_case(sample_inventory):
    # Arrange: fixture includes Electronics and electronics
    # Act
    result = calculate_summary(sample_inventory)
    # Assert
    assert result["category_counts"] == {"electronics": 2, "office supplies": 2}


def test_summary_empty_inventory():
    # Arrange
    inventory = []
    # Act
    result = calculate_summary(inventory)
    # Assert
    assert result == {"unique_items": 0, "total_quantity": 0, "low_stock_items": 0, "category_counts": {}}


@pytest.mark.parametrize("quantity,expected_low_stock", [(4, 1), (5, 0)], ids=["four_is_low", "five_is_not_low"])
def test_low_stock_boundary(quantity, expected_low_stock):
    # Arrange
    inventory = [{"name": "Pen", "category": "Office", "quantity": quantity}]
    # Act
    result = calculate_summary(inventory)
    # Assert
    assert result["low_stock_items"] == expected_low_stock
