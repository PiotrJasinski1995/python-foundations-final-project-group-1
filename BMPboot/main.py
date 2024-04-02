from .address_book import *
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
def add_contact(args, contacts):
    (name,) = args
    contact = Record(name)

    while True:
        input_phone = input('Enter phone number (0: exit, ENTER: skip current):\n')
        if input_phone in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding phone number, email, address and birthday.'
        elif input_phone == '':
            print('Phone number omitted!')
            break
        else:
            try:
                contact.add_phone(input_phone)
                break
            except PhoneFormatException:
                print('Number should contain 10 digits!')

    while True:
        input_email = input('Enter email (0: exit, ENTER: skip current):\n')
        if input_email in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding email, address and birthday.'
        elif input_email == '':
            print('Email omitted!')
            break
        else:
            try:
                contact.add_email(input_email)
                break
            except EmailFormatException:
                print('Wrong email address format!')

    while True:
        input_address = input('Enter address (0: exit, ENTER: skip current):\n')
        if input_address in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding address and birthday.'
        elif input_address == '':
            print('Address omitted!')
            break
        else:
            contact.add_address(input_address)
            break

    while True:
        input_birthday = input('Enter date of birthday in format YYYY-MM-DD (0: exit, ENTER: skip current):\n')
        if input_birthday in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding day of birthday.'
        elif input_birthday == '':
            print('Birthday omitted!')
            break
        else:
            try:
                contact.add_birthday(input_birthday)
                break
            except DateFormatException:
                print('Date should be given in YYYY-MM-DD format!')

    while True:
        input_note = input('Enter a note (0: exit, ENTER: skip current):\n')
        if input_note in ['0']:
            contacts.add_record(contact)
            return 'User exited without adding day of birthday.'
        elif input_note == '':
            print('Note omitted!')
            break
        else:
            input_tag = check_tag()
            contact.add_note(input_tag, input_note)
            break

    contacts.add_record(contact)

    return 'Contact added.'


@input_error
def get_all(args, contacts):
    if len(args) != 0:
        return 'You should not put any arguments in "all" command!'

    if not contacts:
        return 'No contacts in phonebook!!!'

    return get_phonebook_list(contacts)


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


def print_contact(contact, alphabetical=True):
    print('Name: ', str(contact.name), ' | ', end='')
    print('Address: ', str(contact.address), ' | ', end='')
    print('Phone: ', str(contact.phone), ' | ', end='')
    print('Email: ', str(contact.email), ' | ', end='')
    print('Birthday: ', str(contact.birthday), ' | ')
    print('Notes:')

    reverse_flag = False if alphabetical else True

    if contact.notes:
        notes_dict = dict(sorted(contact.notes.items(), key=lambda item: item[0], reverse=reverse_flag))
        for count, note in enumerate(notes_dict, 1):
            note_text = f'\t{str(f'{count})').ljust(3)} {note.ljust(15)} {contact.notes[note]}'
            print(note_text)
    else:
        print('No notes for this contact')
    print('')


@input_error
def find(args, contacts):
    if len(args) == 0:
        return 'Please, enter a value to find! I don\'t know what to look for!'
    else:
        (value,) = args
        print('Searched phrase: ', value, '\n')
        map_id_to_index_dict = {}
        found_contacts = {}
        for key in contacts:
            if str(contacts[key].name) == value:
                found_contacts[key] = contacts[key]

            if str(contacts[key].address) == value:
                found_contacts[key] = contacts[key]

            if str(contacts[key].phone) == value:
                found_contacts[key] = contacts[key]

            if str(contacts[key].email) == value:
                found_contacts[key] = contacts[key]

            if str(contacts[key].birthday) == value:
                found_contacts[key] = contacts[key]
            
            if contacts[key].notes:
                notes_string = ' '.join([note.value for note in contacts[key].notes.values()])

                if value in contacts[key].notes or value in notes_string:
                    found_contacts[key] = contacts[key]

        count = 0
        for key in found_contacts:
            count += 1
            map_id_to_index_dict[count] = key
            if len(found_contacts) < 2:
                continue
            print(count, end=") ")
            print_contact(found_contacts[key], alphabetical=True)

        if count == 0:
            return 'No contacts found.'
        elif count >= 1:
            user_key = 1
            if count > 1:
                while True:
                    user_key = int(input('Which contact do you want to edit/remove? or 0: Exit\n'))

                    if int(user_key) in list(range(len(found_contacts) + 1)):
                        break
                    else:
                        print('You have chosen wrong number!')
            
            alphabetical = True

            while True:
                if user_key == 0:
                    break

                user = map_id_to_index_dict[user_key]
                if count > 1:
                    print(f'You\'ve chosen: ', end=' ')

                print_contact(found_contacts[user], alphabetical=alphabetical)

                sort_text = ''
                option_amount = 4
                alphabetical_text_addition = 'un' if alphabetical == True else ''

                if len(contacts[user].notes) > 1:
                    sort_text = f' | 5: Sort notes {alphabetical_text_addition}alphabetical\n'
                    option_amount += 1

                while True:
                    operation = input('What do you want to do with this contact?\n'
                                    '0: Exit | 1: Change record | 2: Remove record | '
                                    f'3: Remove data from record | 4: Add new note{sort_text}\n')
                    
                    if int(operation) in list(range(option_amount + 1)):
                        break
                    else:
                        print('You have chosen wrong number!')

                if operation in ['0', '']:
                    break
                elif operation == '1':
                    change_fields(user, found_contacts, option='change')
                elif operation == '2':
                    del contacts[user]
                    print("Record deleted.")
                    break
                elif operation == '3':
                    change_fields(user, found_contacts, option='remove')
                elif operation == '4':
                    input_note = input('Enter a note:\n')
                    input_tag = check_tag()
                    contacts[user].add_note(input_tag, input_note)
                elif operation == '5':
                    alphabetical = not alphabetical

        return "Done"
    

def change_fields(user, contacts, option='remove'):
    while True:
        note_text = ''
        if len(contacts[user].notes) > 0:
            note_text += '| 6: Note'

            
        operation = input(f'What field do you want to {option}?\n'
        '0: Exit | 1: Name | 2: Address | 3: Phone | '
        f'4: Email | 5: Birthday {note_text}\n')
        
        if int(operation) in list(range(7)):
            break
        else:
            print('You have chosen wrong number!')
    
    operation_number = int(operation)
    
    fields = ['', 'name', 'address', 'phone', 'email', 'birthday', 'notes']
    dispatch_dict = {'name': Name, 'address': Address, 'phone': Phone, 'email': Email, 'birthday': Birthday, 'note': Note}
    
    if operation in ['0', '']:
        return -1
    elif operation_number in list(range(1, 6)):
        while True:
            question = ''

            if option == 'change':
                question = input(f'Provide a new value for the {fields[operation_number]}: ')
            
            if operation_number == 1:
                setattr(contacts[user], fields[operation_number], dispatch_dict[fields[operation_number]](question))
                break
            else:
                func_name = 'add_' + fields[operation_number]

                try:
                    if option == 'change':
                        func = getattr(contacts[user], func_name)
                        func(question)
                    else:
                        setattr(contacts[user], fields[operation_number], '')                  
                except PhoneFormatException:
                    print('Number should contain 10 digits!')
                except EmailFormatException:
                    print('Wrong email address format!')
                else:
                    break 
    elif operation == '6' and len(contacts[user].notes) > 0:
        notes_dict = {}
        found_notes = contacts[user].notes
        note_text = ''
        count = len(found_notes)

        for count, key in enumerate(found_notes, 1):
            notes_dict[count] = key
            note_text = f'\t{(str(count) + ')').ljust(3)} {key.ljust(15)} {found_notes[key]}'
            print(note_text)

        if count == 1:
            user_key = 1
        elif count > 1:
            note_question = f'Which note do you want to {option}? or 0: Exit\n'

            while True:
                user_key = int(input(f'{note_question}'))     

                if int(user_key) in list(range(len(found_notes) + 1)):
                    break
                else:
                    print("You have chosen wrong number!")

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

                while True:
                    note_operation = input(f'What do you want to do with this note?\n{additional_note_question_text}')   
                    if int(note_operation) in list(range(3)):
                        break
                    else:
                        print("You have chosen wrong number!")
                          
            if option == 'remove':
                note_operation = '3'
         
            if note_operation in ['0', '']:
                break
            elif note_operation == '1':
                new_tag = check_tag()
                actual_note = contacts[user].notes[note]
                contacts[user].notes.pop(note)
                contacts[user].notes[new_tag] = actual_note
                break
            elif note_operation == '2':
                new_note = input('Provide new value for note: ')
                contacts[user].notes[note] = new_note
                break
            elif note_operation == '3':
                contacts[user].notes.pop(note)
                break
            
    
    print(f'Field {option} done.')


def check_tag():
    while True:
        tag = input('Enter a tag:\n')
        
        if len(tag.split(' ')) != 1:
            print('Tag should be one word!')
        elif tag == '':
            print('Tag cannot be empty!')
        else:
            return tag


def main():
    contacts = load_address_book()
    print('Welcome to the assistant bot!')

    while True:
        try:
            user_input = input('Enter a command: ')
            command_input, *args = parse_input(user_input)
            command = ""
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
