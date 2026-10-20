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
The following explanations are my draft understanding and should
be reviewed and rewritten in my own words before submission.

load_inventory() reads each nonblank line and separates it at the
pipe characters. It converts the quantity to an integer and stores
each record as a dictionary in a list. A missing file returns an
empty list.

search_inventory() removes whitespace from the search input and
rejects an empty term. It uses casefold() on both the term and each
item name so capitalization does not affect matching. It collects
partial matches and displays them, or prints a no-match message.