
import time
import os
from apminsight import constants

try:
    from collections.abc import Callable  # noqa
except ImportError:
    from collections import Callable  # noqa

def current_milli_time():
    return int(round(time.time() * 1000))


def is_non_empty_string(string):
    if not isinstance(string, str):
        return False
    elif string == '':
        return False

    return True

def is_empty_string(string):
    if not isinstance(string, str):
        return True
    elif string == '':
        return True

    return False

def is_digit(char):
    if char >= '0' and char <= '9':
        return True

    return False

def is_callable(fn):
    return isinstance(fn, Callable)

def is_ext_comp(component_name):
    return component_name in constants.ext_components


def check_and_create_base_dir():
    base_path = ''
    
    try:
        base_path = os.path.join(os.getcwd(), constants.base_dir)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
    except Exception:
        print('Error while creating agent base dir in '+ os.getcwd())
    
    return base_path



def get_masked_query(sql):
    if is_empty_string(sql):
        return ''

    masked_query = ''
    length = len(sql)
    index = 0
    while index<length:
        char = sql[index]
        if char == '\'' or char == '"':
            char2 = char
            masked_query +='?'
            index+=1
            while index<length:
                char = sql[index]
                if char == '\\' and index < length-1:
                    index+=1
                elif char == char2:
                    break
                    
                index+=1

            if index>= length:
                break

        else:
            if is_digit(char) or ( char == '.' and index < length-1 and is_digit(sql[index+1])):
                masked_query +='?'
                while index < length:
                    char = sql[index]
                    if not is_digit(char) and char!='.':
                        break

                    index+=1

                if index >= length:
                    break

                index-=1

            else:
                if not char.isalpha():
                    if char != '_':
                        masked_query += char
                        index+=1
                        continue

                
                while index < length:
                    char = sql[index]
                    if not char.isalpha() and char!= '_' and not is_digit(char):
                        break

                    masked_query += char
                    index+=1

                if index >= length:
                    break

                index-=1


        index+=1

    return masked_query
