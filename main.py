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
    result = ''
    field_width = 15
    result += "Name".ljust(field_width) + "|" + "Address".ljust(field_width) + "|" + "Phone".ljust(field_width) + \
              "|" + "Email".ljust(field_width) + "|" + "Birthday".ljust(field_width) + "|" + "Notes\n"
    result += "-" * (field_width * 6)

    for key, record in contacts.items():
        result += "\n" + str(record.name).ljust(field_width) + "|" + str(record.address).ljust(field_width) + "|" +\
                  str(record.phone).ljust(field_width) + "|" + str(record.email).ljust(field_width) + "|" + \
                  str(record.birthday).ljust(field_width) + "|" + str(record.notes.tag)

    return result


def get_birthday_contact(contact):
    return {'name': contact.name.value, 'birthday': datetime.strptime(contact.birthday.value, '%d.%m.%Y')}


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return 'Wrong arguments!\n' \
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
def add_contact(args, contacts):  # add contact by add command and only 1 argument [name]
    if len(args) == 0:
        return 'Please, enter a name of contact, which you want to add!'
    name = args[0]
    contact = Record(name)

    # add address
    input_address = input('Enter address: (0 or ENTER to exit)')
    if input_address in ['0', '']:
        contacts.add_record(contact)
        return 'User exited without adding address.'
    contact.add_address(input_address)

    # phone number
    input_phone = input('Enter phone number: (0 or ENTER to exit)')
    if input_address in ['0', '']:
        contacts.add_record(contact)
        return 'User exited without adding phone number.'
    contact.add_phone(input_phone)

    # email
    input_email = input('Enter email: (0 or ENTER to exit)')
    if input_email in ['0', '']:
        contacts.add_record(contact)
        return 'User exited without adding email.'
    contact.add_email(input_email)

    # birthday
    input_birthday = input('Enter date of birthday in format: dd.mm.yyyy (0 or ENTER to exit):')
    if input_birthday in ['0', '']:
        contacts.add_record(contact)
        return 'User exited without adding day of birthday .'
    contact.add_birthday(input_birthday)

    # add contact to contacts
    contacts.add_record(contact)
    save_address_book(contacts)

    return 'Contact added.'


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
            try:
                return pickle.load(file)
            except EOFError:
                print('Address book is empty.')
                return AddressBook()

    return AddressBook()


def help():
    commands = ['Command', '-' * 14, 'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays',
                'hello', 'close or exit']
    arguments = ['Arguments', '-' * 20, '[name] [phone]', '[name] [phone]', '[name] [new phone]', '[name]',
                 'no arguments', '[name]', 'no arguments', 'no arguments', 'no arguments']
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
        help_text += '{command:<14} {argument:<20} {text}\n'.format(command=commands[i], argument=arguments[i],
                                                                    text=texts[i])

    return help_text

# print one contact
def print_contact(contact):
    print('Name: ', contact.name.value, ' | ', end='')
    print('Address: ', contact.address.value, ' | ', end='')
    print('Phone: ', contact.phone.value, ' | ', end='')
    print('Email: ', contact.email.value, ' | ', end='')
    print('Birthday: ', contact.birthday.value, ' | ', end='')
    print('Note: ', end='')
    if hasattr(contact, 'notes'):
        if contact.notes != {}:
            print('tag: ', contact.notes.tag, ' | ', end='')
            print('note: ', contact.notes.note)
    print('')


# add find function
def find(args, contacts):
    # if args is empty return warning
    if len(args) == 0:
        return 'Please, enter a value to find! I don\'t know what to look for!'
    # if args is not empty
    else:
        # get the value from args
        value = args[0]
        print('Searched phrase: ', value)
        # Iterate through contacts
        map_id_to_index_dict = {}
        found_contacts = {}
        for key in contacts:
            # if value is in name
            # print(contacts)
            if contacts[key].name.value == value:
                found_contacts[key] = contacts[key]

            # if value is in address
            if contacts[key].address.value == value:
                found_contacts[key] = contacts[key]

            # if value is in phone
            if contacts[key].phone.value == value:
                found_contacts[key] = contacts[key]

            # if value is in email
            if contacts[key].email.value == value:
                found_contacts[key] = contacts[key]

            # if value is in birthday
            if contacts[key].birthday.value == value:
                found_contacts[key] = contacts[key]
            
            #if value is in note
            if hasattr(contacts[key], 'notes'):
                if contacts[key].notes != {}:
                    if value in contacts[key].notes.tag or value in contacts[key].notes.note:
                        found_contacts[key] = contacts[key]


        # print what was found
        count = 0
        for key in found_contacts:
            count += 1
            print(count, end=") ")
            map_id_to_index_dict[count] = key
            print_contact(found_contacts[key])

        if count == 0:
            return "No contacts found."
        elif count >= 1:
            user_key = 1 #przypisz wartość 1 - wybór pierwszego/jedynego kontaktu
            if count > 1:
                user_key = int(input('Which contact do you want to edit/remove? or 0: Exit '))

            # Loop - what to do with found contacts
            while True:
                if user_key == 0:
                    break

                user = map_id_to_index_dict[user_key]
                if count > 1:
                    print(f"You've chosen: ", end=" ")
                else:
                    print("Found contact: ", end=" ")
                print_contact(found_contacts[user])

                operation = input('What do you want to do with this contact?\n'
                              '0: Exit | 1: Change record | 2: Remove record | '
                              '3: Remove data from record\n')

                if operation in ['0', '']:
                    break
                elif operation == '1':
                    operation = input('What field do you want to change?\n'
                                  '0: Exit | 1: Name | 2: Address | 3: Phone | '
                                  '4: Email | 5: Birthday | 6: Note\n')
                    question = input('Provide a new value for the field: ')
                    if operation in ['0', '']:
                        break
                    elif operation == '1':
                        contacts[user].name = Name(question)
                    elif operation == '2':
                        contacts[user].address = Address(question)
                    elif operation == '3':
                        contacts[user].phone = Phone(question)
                    elif operation == '4':
                        contacts[user].email = Email(question)
                    elif operation == '5':
                        contacts[user].birthday = Birthday(question)
                    elif operation == '6':
                        noteKey = input('Provide a tag for the note: ')
                        if noteKey == '':
                            noteKey = 'Default tag name'
                        contacts[user].notes = Notes(noteKey, question)
                    print("Field changed.")
                elif operation == '2':
                    del contacts[user]
                    print("Record deleted.")
                elif operation == '3':
                    question = input('What field do you want to remove?\n'
                                 '0: Exit | 1: Address | 2: Phone | '
                                 '3: Email | 4: Birthday | 5: Note\n')
                    if question in ['0', '']:
                        break
                    elif question == '1':
                        contacts[user].address.value = ""
                    elif question == '2':
                        contacts[user].phone.value = ""
                    elif question == '3':
                        contacts[user].email.value = ""
                    elif question == '4':
                        contacts[user].birthday.value = ""
                    elif question == '5':
                        pass
                    print("Field removed.")

                save_address_book(contacts)

        return "Done"

# end find function________________________


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
            # add find command
            elif command == 'find':
                print(find(args, contacts))
            else:
                print('Invalid command.')
        except ValueError:
            print('Please use commands!')

    save_address_book(contacts)


if __name__ == '__main__':
    main()
