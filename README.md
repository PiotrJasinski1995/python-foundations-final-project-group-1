# Address Book Assistant

Address Book Assistant is a simple program for managing an address book, written in Python.

## Table of Contents

- [Description](#description)
- [Install Package](#install)
- [Usage Instructions](#usage-instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Author](#author)

## Description

Address Book Assistant allows the user to add, search, browse, and manage contacts in an address book. The program supports various fields such as name, address, phone number, email, date of birth, and notes.

## Install

To install the package from pip, run the following command:
pip install BMPboot
Example of usage - it starts the program:

from BMPboot import main

main.main()
{}

## Usage Instructions

To run the program, execute the `main.py` file. Upon running, the user can issue commands via the command line interface. Available commands include adding new contacts, searching for existing contacts, browsing all contacts in the address book, displaying upcoming birthdays, and more.

## Examples

### Adding a New Contact

Enter a command: add John
Enter phone number (0: exit, ENTER: skip current):
1234567890
Enter email (0: exit, ENTER: skip current):
john@example.com
Enter address (0: exit, ENTER: skip current):
123 Main Street
Enter date of birthday in format YYYY-MM-DD (0: exit, ENTER: skip current):
1990-01-01
Enter a note (0: exit, ENTER: skip current):
Best friend

### Searching for a Contact

Enter a command: find John
Searched phrase: John

Name: John | Address: 123 Main Street | Phone: 1234567890 | Email: john@example.com | Birthday: 1990-01-01 |
Notes:

1. Best friend

### Displaying Upcoming Birthdays

Enter a command: birthdays 7
Name | Birthday
John | 1990-01-01

## Requirements

To run the program, you need a Python 3.x interpreter and the library: thefuzz (pip install thefuzz'.

## Author

The program was written by:

- Piotr Jasiński
- Michał Pokracki
- Bartosz Zygmunt

```

```
