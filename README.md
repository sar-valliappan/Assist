# Transferology - California Transfer Courses Lookup

This Python project allows you to retrieve course articulation information between California community colleges and universities.

I wanted to take a community college class over the summer to satisfy prerequisites for a class next fall. However, there's no easy way to search for all the community colleges that offer that class.

Assist.org currently only allows a user to search for what course at a selected 4-year university is equivalent to a given course at a community college. There is no way to reverse this search, allowing the user to search for all community college courses that are equivalent to a given course at a 4-year university. This project aims to fix that.

---

## Features

- Search for course equivalencies by **receiving institution**, **prefix**, and **course number**.
- Supports **community college to university articulation** lookups.
- Correctly parses **prerequisite groups** with `AND` / `OR` logic.
- Handles all colleges with agreements with the target institution in a single run.
- Fully API-based — no browser automation required.

---

## Requirements

- Python 3.8+
- Modules:
  - `urllib` (built-in)
  - `ssl` (built-in)
  - `certifi`
  - `json` (built-in)
  - `time` (built-in)

Install `certifi` if needed using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---
## Usage

### Run the script:
```bash
python assist_lookup.py
```
Output:
```bash
Enter the receiving institution acronym:
Prefix:
Number:
```
Example Input:
```bash
Receiving institution (type acronym): UCSD
Prefix: CSE
Number: 12
```
The script will fetch articulation agreements for all California community colleges and print results in the format:
```bash
Evergreen Valley College
(CIS 255 AND COMSC 171) OR COMSC 200
```

---

## How It Works

1. The script retrieves institution IDs from the ASSIST API.

2. For each sending institution (community college), it fetches the prefix key.

3. It queries the Articulation API using that prefix key.

3. It finds the target course and extracts prerequisite groups.

4. Prerequisite groups are combined according to the group-level conjunctions (AND / OR).


## Future Enhancements

1. Add a link to that class's course schedule to verify if it is being offered.

2. Add filtering for online versus in-person classes.

3. Add filtering for specific cities and regions.
