# AI Usage Report

## Tools Used
OpenAI ChatGPT/Codex.

## How AI Was Used
AI helped interpret the requirements, suggested Python functions,
explained lists and dictionaries, diagnosed indentation errors,
provided Git workflow guidance, drafted documentation, and supplied
a temporary automated verification script.

## Example Prompts
- "Keeping till ICA 6 from memory in mind make me finish this homework."
- "Which lines do I paste these on?"
- "What's the mistake?"

## Suggestions Accepted
I used suggestions for loading pipe-separated records, validating
input, rejecting duplicate names with casefold(), searching names,
calculating summaries, and testing normal and invalid cases.

## Suggestions Rejected or Modified
I chose to enter and integrate the changes myself rather than have
the assistant directly edit the project. When pasted code had
incorrect indentation, I corrected its placement and spacing before
rerunning it. The temporary unavailable-feature messages used during
development were replaced as the features were implemented.

## Verification
I ran the application interactively while adding features.
I also ran an AI-assisted verification script that tested 18 cases
using supplied inputs, captured output, assertions, and temporary
files. All 18 checks passed. TESTING.md describes the actual checks.
I checked Git status and pushed completed work to GitHub.

## Code Understanding

load_inventory() gets the saved items from the text file. It splits
each line at the | symbols to separate the name, category, and
quantity. It changes the quantity from text into an integer and
puts each item's dictionary into a list. If the file is missing,
it returns an empty list so the program can still start.

search_inventory() asks what item the user wants to find. It removes
extra spaces at the beginning and end and rejects a blank search.
It uses casefold() so uppercase and lowercase letters match.
It checks whether the search text appears anywhere in each item
name, then displays all matches or a message saying none were found.