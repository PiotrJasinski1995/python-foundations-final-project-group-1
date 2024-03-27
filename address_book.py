from collections import UserDict
import re
import nanoid


class PhoneFormatException(Exception):
    pass


class EmailFormatException(Exception):
    pass


class DateFormatException(Exception):
    pass


class ContactExistsError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Address(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        match = re.fullmatch('\\d{10}', value)

        if match == None:
            raise PhoneFormatException

        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        email_validate_pattern = r"^\S+@\S+\.\S+$"
        match = re.fullmatch(email_validate_pattern, value)

        if match == None:
            raise EmailFormatException

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        match = re.fullmatch('\\d{2}.\\d{2}.\\d{4}$', value)

        if match == None:
            raise DateFormatException

        super().__init__(value)


class Notes(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.id = nanoid.generate()
        self.name = Name(name)
        self.address = None
        self.phone = None
        self.email = None
        self.birthday = None
        self.notes = [{}]  # dict of notes {tagname: note}

    def __str__(self):
        return f'Contact name: {self.name.value}, phone: {self.phone}'

    def add_address(self, address):
        self.address = Address(address)

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_note(self, notes):
        self.notes = Notes(notes)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.id] = record

    def find(self, name):
        if self.data.get(name, False):
            return self.data[name]

        return -1
