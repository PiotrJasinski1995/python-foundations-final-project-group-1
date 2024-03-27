from address_book import *
from birthday_function import get_birthday_per_week
from datetime import datetime
import pickle
from pathlib import Path


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def get_phonebook_list(contacts):
    contact_name = 'Contact'
    max_key_len = max(len(key) for key in contacts)
    max_key_len = len(contact_name) if len(contact_name) > max_key_len else max_key_len
    max_key_len = max_key_len + 1 if not max_key_len % 2 else max_key_len

    phone_name = 'Phone'
    max_contact_len = max(len(contacts[key].phone.value) for key in contacts)
    max_contact_len = len(phone_name) if len(phone_name) > max_contact_len else max_contact_len
    max_contact_len = max_contact_len + 1 if not max_contact_len % 2 else max_contact_len

    space_width = 4
    separator = f'|{'-' * ((max_key_len + max_contact_len) + 2 * space_width + 1)}|\n'

    contacts_string = f'\n{separator}'
    title_name = 'PHONEBOOK'
    pound_sign_string_len = int((len(separator) - len(title_name)) / 2)
    contacts_string += f'| {'#' * (pound_sign_string_len - 3)} {title_name} {'#' * (pound_sign_string_len - 3)} |\n'
    contacts_string += separator
        
    contacts_string += '|{name:^{name_width}}|{phone:^{phone_width}}|\n'.format(name=contact_name, name_width=max_key_len + space_width, phone=phone_name, phone_width=max_contact_len + space_width)
    contacts_string += separator * 2

    for key in contacts:
        contacts_string += '|{name:^{name_width}}|{phone:^{phone_width}}|\n'.format(name=key, name_width=max_key_len + 4, phone=contacts[key].phone.value, phone_width=max_contact_len + 4)
        contacts_string += separator

    return contacts_string


def get_birthday_contact(contact):  
    return {'name': contact.name.value, 'birthday': datetime.strptime(contact.birthday.value, '%d.%m.%Y')}


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return 'Wrong arguments!\n'\
                'Type "help" for more info.'
        except KeyError:
            return 'Contact does not exists!'
        except PhoneFormatException:
            return 'Number should contain 10 digits!'
        except EmailFormatException:
            return 'Wrong email address format!'
        except DateFormatException:
            return 'Date should be given in DD.MM.YYYY format!'
        except ContactExistsError:
            return 'Contact already exists!'
    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args

    if contacts.find(name) == -1:
        contact = Record(name)
        contact.add_phone(phone)
        contacts.add_record(contact)
        return 'Contact added.'
    
    raise ContactExistsError


@input_error      
def change_contact(args, contacts):
    name, phone = args 
    contacts[name].add_phone(phone)

    return 'Contact changed.'
          

@input_error
def get_phone(args, contacts):
    (name,) = args
    
    return f'Phone number for {name}: {contacts[name].phone}'


@input_error   
def get_all(args, contacts):
    if len(args) != 0:
        return 'You should not put any arguments in "all" command!'
    
    if not contacts:
        return 'No contacts in phonebook!!!'
    
    return get_phonebook_list(contacts)


@input_error
def add_birthday(args, contacts):
    name, birthday = args
    contacts[name].birthday = Birthday(birthday)
    
    return f'Birthday for {name} added.'


def get_birthday(args, contacts):
    (name,) = args

    if contacts[name].birthday == None:
        return 'No birthday added for this contact!'
    
    return f'Birthday for {name}: {contacts[name].birthday}'

  
def get_birthdays(args, contacts):
    if len(args) != 0:
        return 'You should not put any arguments in "birthdays" command!'
    
    if not contacts:
        return 'No contacts in phonebook!!!'
    
    filter_list = filter(lambda contact: contact.birthday != None, contacts.data.values())
    contact_dict = map(get_birthday_contact, filter_list)
    return get_birthday_per_week(contact_dict)


def save_address_book(contacts):
    file_name = 'address_book.bin'

    with open(file_name, 'wb') as file:
        pickle.dump(contacts, file)


def load_address_book():
    file_name = 'address_book.bin'
    file_path = Path(f'./{file_name}')

    if file_path.is_file():
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    
    return AddressBook()


def help():
    commands = ['Command', '-' * 14, 'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays', 'hello', 'close or exit']
    arguments = ['Arguments', '-' * 20, '[name] [phone]', '[name] [phone]', '[name] [new phone]', '[name]', 'no arguments', '[name]', 'no arguments', 'no arguments', 'no arguments']
    texts = ['Help text',
             '-' * 10,
             'Add a new contact with a name and phone number.',
             'Change the phone number for the specified contact.',
             'Show the phone number for the specified contact.',
             'Show all contacts in the address book.',
             'Add a date of birth for the specified contact.',
             'Show the date of birth for the specified contact.',
             'Show birthdays that will take place within the next week.',
             'Receive a greeting from a bot.',
             'Close the app.']
    
    help_text = '\n'

    for i in range(len(commands)):
        help_text += '{command:<14} {argument:<20} {text}\n'.format(command=commands[i], argument=arguments[i], text=texts[i])

    return help_text


def main():
    contacts = load_address_book()
    print('Welcome to the assistant bot!')

    while True:
        try:
            user_input = input('Enter a command: ')
            command, *args = parse_input(user_input)

            if command in ['close', 'exit']:
                print('Goodbye!')
                break
            elif command == 'hello':
                print('How can I help you?')
            elif command == 'add':
                print(add_contact(args, contacts))
            elif command == 'change':
                print(change_contact(args, contacts))
            elif command == 'phone':
                print(get_phone(args, contacts))
            elif command == 'all':
                print(get_all(args, contacts))
            elif command == 'add-birthday':
                print(add_birthday(args, contacts))
            elif command == 'show-birthday':
                print(get_birthday(args, contacts))
            elif command == 'birthdays':
                print(get_birthdays(args, contacts))
            elif command == 'help':
                print(help())
            else:
                print('Invalid command.')   
        except ValueError:
            print('Please use commands!')

    save_address_book(contacts)


if __name__ == '__main__':
    main()
