from address_book import *
from datetime import datetime, timedelta
import pickle
from pathlib import Path
from thefuzz import process


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def get_phonebook_list(contacts):
    result = ''
    field_width = 20
    result += "Name".ljust(field_width) + "|" + "Address".ljust(field_width) + "|" + "Phone".ljust(12) + \
              "|" + "Email".ljust(field_width) + "|" + "Birthday".ljust(12) + "|" + "Notes\n"
    result += "-" * (field_width * 6)

    for record in contacts.values():
        result += "\n" + str(record.name).ljust(field_width) + "|" + str(record.address).ljust(field_width) + "|" + \
                  str(record.phone).ljust(12) + "|" + str(record.email).ljust(field_width) + "|" + \
                  str(record.birthday).ljust(12) + "|" + str(len(record.notes))

    return result


def get_birthday_contact(contact):
    return {'name': contact.name.value, 'birthday': contact.birthday.value}


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
            return 'Date should be given in YYYY-MM-DD format!'
        except ContactExistsError:
            return 'Contact already exists!'

    return inner


@input_error
def add_contact(args, contacts):  # add contact by add command and only 1 argument [name]
    (name,) = args
    # if len(args) == 0:
    #     return 'Please, enter a name of contact, which you want to add!'
    # name = args[0]
    contact = Record(name)

    # phone number
    while True:
        input_phone = input('Enter phone number (0: exit, ENTER: skip current):\n')
        if input_phone in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding phone number, email, address and birthday.'
        elif input_phone == '':
            print('Phone number omitted!')
            break
        else:  # if phone number is not empty
            try:
                contact.add_phone(input_phone)
                break
            except PhoneFormatException:
                print('Number should contain 10 digits!')

    # email
    while True:
        input_email = input('Enter email (0: exit, ENTER: skip current):\n')
        if input_email in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding email, address and birthday.'
        elif input_email == '':
            print('Email omitted!')
            break
        else:  # if email is not empty
            try:
                contact.add_email(input_email)
                break
            except EmailFormatException:
                print('Wrong email address format!')

    # add address
    while True:
        input_address = input('Enter address (0: exit, ENTER: skip current):\n')
        if input_address in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding address and birthday.'
        elif input_address == '':
            print('Address omitted!')
            break
        else:  # if address is not empty
            contact.add_address(input_address)
            break

    # birthday
    while True:
        input_birthday = input('Enter date of birthday in format YYYY-MM-DD (0: exit, ENTER: skip current):\n')
        if input_birthday in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding day of birthday.'
        elif input_birthday == '':
            print('Birthday omitted!')
            break
        else:  # if birthday is not empty
            try:
                contact.add_birthday(input_birthday)
                break
            except DateFormatException:
                print('Date should be given in YYYY-MM-DD format!')

    # note
    while True:
        input_note = input('Enter a note (0: exit, ENTER: skip current):\n')
        if input_note in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding day of birthday.'
        elif input_note == '':
            print('Note omitted!')
            break
        else:
            input_tag = input('Enter a tag:\n')
            contact.add_note(input_tag, input_note)
            break

    # add contact to contacts
    contacts.add_record(contact)
    # save_address_book(contacts)

    return 'Contact added.'


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


def get_birthdays(args, contacts):
    (days_text,) = args

    days = int(days_text)

    if not contacts:
        return 'No contacts in phonebook!!!'

    filter_list = filter(lambda contact: contact.birthday != '', contacts.data.values())
    filter_list = list(filter_list)
    filter_list = filter(lambda contact: check_birthday(contact.birthday.value, days), filter_list)
    contact_dict = list(map(get_birthday_contact, filter_list))

    if not contact_dict:
        return 'No celebration in this data range'

    field_width = 15
    birthday_text = ''
    birthday_text += "Name".ljust(field_width) + "|" + "Birthday".ljust(field_width) + "\n"
    birthday_text += "-" * (field_width * 2)

    for contact in contact_dict:
        birthday_text += "\n" + str(contact['name']).ljust(field_width) + "|" + str(contact['birthday']).ljust(
            field_width)

    return birthday_text


def check_birthday(string_date, days):
    current_date = datetime.today().date()
    birthday_date = datetime.strptime(string_date, '%Y-%m-%d').date()
    stop_date = current_date + timedelta(days=days)
    birthday_date = birthday_date.replace(year=current_date.year)

    if birthday_date < current_date:
        birthday_date = birthday_date.replace(year=current_date.year + 1)

    return birthday_date <= stop_date


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
    commands = ['Command', '-' * 14, 'add', 'find', 'all', 'birthdays',
                'hello', 'close or exit']
    arguments = ['Arguments', '-' * 20, '[name] [phone]', 'field value', '[name]', '[days]', 'no arguments', 'no arguments']
    texts = ['Help text',
             '-' * 10,
             'Add a new contact with a name and phone number.',
             'Find records based on specific fields [name/phone/email/address/birthday/tag/note].',
             'Show all contacts in the address book.',
             'Show birthdays that will take place within specified number of days from the current date.',
             'Receive a greeting from a bot.',
             'Close the app and save the changes.']

    help_text = '\n'

    for i in range(len(commands)):
        help_text += '{command:<14} {argument:<20} {text}\n'.format(command=commands[i], argument=arguments[i],
                                                                    text=texts[i])

    return help_text


# print one contact
def print_contact(contact):
    print('Name: ', str(contact.name), ' | ', end='')
    print('Address: ', str(contact.address), ' | ', end='')
    print('Phone: ', str(contact.phone), ' | ', end='')
    print('Email: ', str(contact.email), ' | ', end='')
    print('Birthday: ', str(contact.birthday), ' | ')
    print('Notes:')

    if contact.notes:
        for count, note in enumerate(contact.notes, 1):
            note_text = f'{str(f'{count})').ljust(3)} {note.ljust(15)} {contact.notes[note]}'
            print(note_text)
    else:
        print('No notes for this contact')
    print('')


# add find function
@input_error
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
            if str(contacts[key].name) == value:  # if value is '' then error
                found_contacts[key] = contacts[key]

            # if value is in address
            if str(contacts[key].address) == value:
                found_contacts[key] = contacts[key]

            # if value is in phone
            if str(contacts[key].phone) == value:
                found_contacts[key] = contacts[key]

            # if value is in email
            if str(contacts[key].email) == value:
                found_contacts[key] = contacts[key]

            # if value is in birthday
            if str(contacts[key].birthday) == value:
                found_contacts[key] = contacts[key]

            # if value is in note
            # if hasattr(contacts[key], 'notes'):
            #     if contacts[key].notes != {}:
            #         for note in contacts[key].notes.values():
            #             if value in note.tag or value in note.note:
            #                 found_contacts[key] = contacts[key]
            
            if contacts[key].notes:
                if value in contacts[key].notes or value in contacts[key].notes.values():
                    found_contacts[key] = contacts[key]

        # print what was found
        count = 0
        for key in found_contacts:
            count += 1
            map_id_to_index_dict[count] = key
            if len(found_contacts) < 2:
                continue
            print(count, end=") ")
            print_contact(found_contacts[key])

        if count == 0:
            return 'No contacts found.'
        elif count >= 1:
            user_key = 1  # przypisz wartość 1 - wybór pierwszego/jedynego kontaktu
            if count > 1:
                user_key = int(input('Which contact do you want to edit/remove? or 0: Exit '))

                if int(user_key) not in list(range(0, len(found_contacts))):
                    return 'You have chosen wrong number!'

            # Loop - what to do with found contacts
            while True:
                if user_key == 0:
                    break

                user = map_id_to_index_dict[user_key]
                if count > 1:
                    print(f'You\'ve chosen: ', end=' ')
                else:
                    print('Contact:')
                print_contact(found_contacts[user])

                operation = input('What do you want to do with this contact?\n'
                                  '0: Exit | 1: Change record | 2: Remove record | '
                                  '3: Remove data from record | 4: Add new note\n')

                if operation in ['0', '']:
                    break
                elif operation == '1':
                    change_fields(user, found_contacts, option='change')
                    # operation = input('What field do you want to change?\n'
                    #                   '0: Exit | 1: Name | 2: Address | 3: Phone | '
                    #                   '4: Email | 5: Birthday | 6: Note\n')
                    # question = input('Provide a new value for the field: ')
                    # if operation in ['0', '']:
                    #     break
                    # elif operation == '1':
                    #     contacts[user].name = Name(question)
                    # elif operation == '2':
                    #     contacts[user].address = Address(question)
                    # elif operation == '3':
                    #     contacts[user].phone = Phone(question)
                    # elif operation == '4':
                    #     contacts[user].email = Email(question)
                    # elif operation == '5':
                    #     contacts[user].birthday = Birthday(question)
                    # elif operation == '6':
                    #     note_key = input('Provide a tag for the note: ')
                    #     if contacts[user].notes.get(note_key):
                    #         contacts[user].notes[note_key].note = question
                    #     else:
                    #         print("Note with provided tag does not exist.")
                    #         continue
                    # print("Field changed.")
                elif operation == '2':
                    del contacts[user]
                    print("Record deleted.")
                    break
                elif operation == '3':
                    change_fields(user, found_contacts, option='remove')
                #     question = input('What field do you want to remove?\n'
                #                      '0: Exit | 1: Address | 2: Phone | '
                #                      '3: Email | 4: Birthday | 5: Note\n')
                #     if question in ['0', '']:
                #         break
                #     elif question == '1':
                #         contacts[user].address.value = ""
                #     elif question == '2':
                #         contacts[user].phone.value = ""
                #     elif question == '3':
                #         contacts[user].email.value = ""
                #     elif question == '4':
                #         contacts[user].birthday.value = ""
                #     elif question == '5':
                #         note_key = input('Provide a tag for the note: ')
                #         if contacts[user].notes.get(note_key):
                #             contacts[user].notes.pop(note_key)
                #         else:
                #             print("Note with provided tag does not exist.")
                #             continue
                #     print("Field removed.")
                elif operation == '4':
                    input_note = input('Enter a note:\n')
                    input_tag = input('Enter a tag:\n')
                    contacts[user].add_note(input_tag, input_note)

        return "Done"
    

# end find function________________________
@input_error
def change_fields(user, contacts, option='remove'):
    operation = input(f'What field do you want to {option}?\n'
                    '0: Exit | 1: Name | 2: Address | 3: Phone | '
                    '4: Email | 5: Birthday | 6: Note\n')
    
    operation_number = int(operation)
    
    fields = ['', 'name', 'address', 'phone', 'email', 'birthday', 'notes']
    dispatch_dict = {'name': Name, 'address': Address, 'phone': Phone, 'email': Email, 'birthday': Birthday, 'note': Note}
    
    if operation in ['0', '']:
        return -1
    elif operation_number in list(range(1, 6)):
        question = ''

        if option == 'change':
            question = input(f'Provide a new value for the {fields[operation_number]}: ')

        setattr(contacts[user], fields[operation_number], dispatch_dict[fields[operation_number]](question))
    elif operation == '6':
        notes_dict = {}
        found_notes = contacts[user].notes

        count = len(found_notes)

        if count == 1:
            user_key = 1
        elif count > 1:
            user_key = int(input(f'Which note do you want to {option}? or 0: Exit\n'))

        for count, key in enumerate(found_notes, 1):
            notes_dict[count] = key
            note_text = f'{(str(count) + ')').ljust(3)} {key.ljust(15)} {found_notes[key]}'
            print(f'{note_text}')
               

        if int(user_key) not in list(range(1, len(found_notes) + 1)):
            return "You have chosen wrong number!"
        
        ##############################################################################################################################
        # Loop - what to do with found notes
        while True:
            if user_key == 0:
                break

            note = notes_dict[user_key]
            if len(notes_dict) > 1:
                print(f"You've chosen note: ", note)
            else:
                print("Found note: ", note)

            if option == 'change':
                additional_note_question_text = '0: Exit | 1: Change tag | 2: Change note \n'
                note_operation = input(f'What do you want to do with this note?\n{additional_note_question_text}')         

            if option == 'remove':
                note_operation = '3'
         

            if note_operation in ['0', '']:
                break
            elif note_operation == '1':
                new_tag = input('Provide new tag for note')
                actual_note = contacts[user].notes[note]
                contacts[user].notes.pop(note)
                contacts[user].notes[new_tag] = actual_note
                break
            elif note_operation == '2':
                new_note = input('Provide new value for note')
                contacts[user].notes[note] = new_note
                break
            elif note_operation == '3':
                contacts[user].notes.pop(note)
                break
            
    print(f'Field {option}d.')


def main():
    contacts = load_address_book()
    print('Welcome to the assistant bot!')

    while True:
        try:
            user_input = input('Enter a command: ')
            command_input, *args = parse_input(user_input)
            command = ""

            # thefuzz
            choices = ['close', 'exit', 'hello', 'add', 'phone', 'all', 'show-birthday', 'birthdays', 'help', 'find']
            fuzz_command = process.extractOne(command_input, choices=choices, score_cutoff=60)
            if fuzz_command is not None:
                command = fuzz_command[0]
                if int(fuzz_command[1]) < 100:
                    confirmation = input(f'Did you mean "{fuzz_command[0]}"? [Y/N]\n').lower()
                    if confirmation != 'y':
                        command = None

            if command in ['close', 'exit']:
                print('Goodbye!')
                break
            elif command == 'hello':
                print('How can I help you?')
            elif command == 'add':
                print(add_contact(args, contacts))
            elif command == 'all':
                print(get_all(args, contacts))
            elif command == 'birthdays':
                print(get_birthdays(args, contacts))
            elif command == 'help':
                print(help())
            elif command == 'find':
                print(find(args, contacts))
            else:
                print('Invalid command.')
        except ValueError:
            print('Please use commands!')

    save_address_book(contacts)


if __name__ == '__main__':
    main()
