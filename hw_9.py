import os
import sys
import re


# Constants
FULL_LEN_NUMBER = 12
SHORT_LEN_NUMBER = 10
class ContactExist(Exception):
    pass

class ContactNotExist(Exception):
    pass

class UncorrectPhoneNumber(Exception):
    pass
class TypeValue(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeValue:
            return 'Uncorrect format of a concact!!! \nExample: \n         add/change contact_name phone_number'
        except ContactExist:
            return 'Contact is already existed!!! \nExample: \n         add new_contact_name new_phone_number'
        except ContactNotExist:
            return 'Contact is not exist :('
        except UncorrectPhoneNumber:
            return 'Uncorrect type of number :('
        except:
            return rise_eroor()
    return inner

def format_phone_number(func,full_len_number = FULL_LEN_NUMBER, short_len_number = SHORT_LEN_NUMBER):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if len(result) == FULL_LEN_NUMBER:
            result = f'+{result}'
        elif len(result) == SHORT_LEN_NUMBER:
            result = f'+38{result}'
        else:
            raise UncorrectPhoneNumber
        return result
    return inner

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = ''.join(re.findall("[0-9]",phone))
    return new_phone

def rise_eroor(*args, **kwargs):
    return f'Error command or uncorrect format'

def findComand(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return inner

def comand_Close(*args, **kwargs):
    sys.exit(f'Good bye!')

def comand_Hello(*args, **kwargs):
    return 'How can I help you?'

@input_error
def comand_Add(name_str,phone_number, *args, **kwargs):
    if not name_str or not phone_number:
        raise TypeValue
    if not concacts_dict.get(name_str):
        phone_number = sanitize_phone_number(phone_number)
        concacts_dict[name_str] = (phone_number)
    else:
        raise ContactExist
    return f'Successfully added {name_str} with number {phone_number}'

@input_error
def comand_Change(name_str, phone_number, *args, **kwargs):
    if not name_str or not phone_number:
        raise TypeValue
    if concacts_dict.get(name_str):
        phone_number = sanitize_phone_number(phone_number)
        concacts_dict[name_str] = (phone_number)
    else:
        raise ContactNotExist
    return f'Successfully changed {name_str} on number {phone_number}'

@input_error
def comand_Phone(name_str, *args, **kwargs):
    if not name_str:
        raise IndexError
    if concacts_dict.get(name_str):
        return concacts_dict[name_str]
    else:
        raise ContactNotExist


def comandShowAll(*args, **kwargs):
    result = ''
    for key in concacts_dict:
        result += '{:<10} -> {}\n'.format(key, concacts_dict[key])
    return result

concacts_dict = {}

comand_dict = {
    'good bye': comand_Close,
    'close': comand_Close,
    'exit': comand_Close,
    'hello': comand_Hello,
    'add': comand_Add,
    'change': comand_Change,
    'phone': comand_Phone,
    'show all': comandShowAll
}

def get_handler(operator):
    return comand_dict.get(operator, rise_eroor)

def main():
    while True:
        inp = input("Write command: ")
        s1 = None
        s2 = None
        if not inp.lower() in ['good bye', 'show all']:
            inp = inp.split(' ')
            command = inp[0].lower()
            if len(inp)==3:
                s1 = inp[1]
                s2 = inp[2]
            elif len(inp) == 2:
                s1 = inp[1]
        else:
            command = inp.lower()
        handler = get_handler(command)
        h = handler(s1, s2)
        print(h)

if __name__ == "__main__":
    main()
