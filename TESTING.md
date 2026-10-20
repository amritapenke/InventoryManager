# Inventory Manager Testing

## Method
On October 20, 2026, I ran an AI-assisted Python verification script
against the application functions. It supplied inputs, captured output,
and checked returned values and inventory changes. Temporary files
were used for file tests without changing the submitted sample data.
All 18 automated checks passed.

| # | Feature | Input or Action | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|
| 1 | Missing file | Load a nonexistent temporary file | Return an empty list | Returned [] | Pass |
| 2 | Empty inventory | View an empty list | Display no-items message | Correct message displayed | Pass |
| 3 | Add item | HDMI Cable, Electronics, 6 | Add dictionary with integer quantity | Correct item added | Pass |
| 4 | Empty name | Submit an empty name | Reject without changing inventory | Returned False; list unchanged | Pass |
| 5 | Duplicate name | Add hdmi cable after HDMI Cable | Reject despite capitalization difference | Duplicate rejected; list unchanged | Pass |
| 6 | Invalid quantity | Enter six | Reject without changing inventory | Returned False; list unchanged | Pass |
| 7 | Negative quantity | Enter -1 | Reject without changing inventory | Returned False; list unchanged | Pass |
| 8 | Update quantity | Select item 1; enter 15 | Update first item's quantity | Quantity became 15 | Pass |
| 9 | Invalid selection | Update item 99 | Reject and preserve inventory | Returned False; list unchanged | Pass |
| 10 | Remove item | Remove item 2 | Remove USB-C Charger | Selected item removed | Pass |
| 11 | Partial search | Search CHARGER | Display both chargers, excluding paper | Both chargers displayed; paper excluded | Pass |
| 12 | No-match search | Search zzzz | Display no-match message | Correct message displayed | Pass |
| 13 | Summary | Five-item fixture totaling 50; mixed-case category names | Show 5 items, 50 units, 2 low-stock items; category counts 2, 2, 1 | All expected values displayed | Pass |
| 14 | File persistence | Save changed inventory and load it again | Reload identical records | Reloaded list matched saved list | Pass |
| 15 | Blank search | Enter spaces only | Reject empty search | Correct error displayed | Pass |
| 16 | Empty removal | Remove from an empty list | Return False | Returned False | Pass |
| 17 | Empty update | Update an empty list | Return False | Returned False | Pass |
| 18 | Invalid removal | Enter abc as the item number | Return False without crashing | Returned False | Pass |

## Manual Checks
During development, I also ran the menu interactively and checked:
- Numbered inventory display.
- Invalid menu option 9.
- Adding HDMI Cable and seeing it after restarting.
- Updating Laptop Charger to quantity 12.
- Duplicate-name and nonnumeric-quantity rejection.
- Summary output: 5 items, total quantity 50, and 2 low-stock items.
- Normal exit using option 7.

## Problems Corrected
Initial menu and summary edits produced indentation errors.
I corrected the indentation, saved the files, and reran the program.
The final automated verification completed without failures.