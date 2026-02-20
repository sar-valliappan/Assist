# ASSIST Course Lookup

This Python project allows you to query the ASSIST API and retrieve course articulation information between California community colleges and universities.

Assist.org currently does not have the functionality to search for what community college courses correlate to a given 4-year university course, only the other way around. This project aims to fix that.

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
