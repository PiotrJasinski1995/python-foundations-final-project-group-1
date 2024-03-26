from collections import UserDict
import re


class PhoneFormatException(Exception):
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


class Phone(Field):
    def __init__(self, value):
        match = re.fullmatch('\\d{10}', value)

        # Exception for future error handling
        if match == None:
            raise PhoneFormatException

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        match = re.fullmatch('\\d{2}.\\d{2}.\\d{4}$', value)

        # Exception for future error handling
        if match == None:
            raise DateFormatException

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = ''
        self.birthday = None

    def __str__(self):
        return f'Contact name: {self.name.value}, phone: {self.phone}'

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_birthday(self, birthday):
        self.birthday =  Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        if self.data.get(name, False):
            return self.data[name]
        
        return -1
