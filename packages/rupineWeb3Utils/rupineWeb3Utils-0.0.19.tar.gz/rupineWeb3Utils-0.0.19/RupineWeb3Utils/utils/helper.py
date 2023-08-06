import json
import os
import sys
import time
import datetime
from pandas.core.frame import DataFrame

from web3 import Web3
from collections import deque

def datetime_string_to_datetime(datetime_string:str):
    '''
    utils helper method: string to datetime type

    Parameters
    --------
    datetime_string : str
        string of datetime with format %Y-%m-%d %H:%M:%S.%f
    
    Results
    --------
    datetime
    '''
    t = time.strptime(datetime_string,'%Y-%m-%d %H:%M:%S.%f')
    ts = time.mktime(t)
    d = datetime.datetime.fromtimestamp(ts)
    return d

def split_string(string:str,delimiter:str=','):
    '''
    utils helper method: split string by delimiter

    Parameters
    --------
    string : str
        string to split
    delimiter : str
        delimiter character
    
    Results
    --------
    list
    '''
    return string.split(delimiter)

def compare_dictionaries(d1:dict,d2:dict):
    '''
    utils helper method: compare two dictionaries and return 

    Parameters
    --------
    d1 : dict
        first dictionary
    d1 : dict
        second dictionary
    
    Results
    --------
    list
        added, removed, modified, same
    '''
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    removed = d1_keys - d2_keys
    added = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same

def check_if_event_changes_window_state(key_list:list,comparison:tuple,added=False,removed=False,modified=False,same=False):
    states = [added,removed,modified,same]
    for idx,s in enumerate(states):
        if s:
            for item in key_list:
                if item in comparison[idx]:
                    return True
    return False

def replace_or_create_key_in_dictionary_from_value(dictionary:dict,new_key:str,value:any):
    '''
    utils helper method: if dictionary has a key, the new value is initialised. If key
    does not exist, new key is created with value.

    Parameters
    --------
    
    dictionary : dict
        dictionary 
    new_key : str
        name of the new key
    value : any
        value of any datatype
    
    Results
    --------
    dict
        modified dictionary
    '''
    if value in dictionary.values():
        old_key = [k for k,v in  dictionary.items() if v == value][0]
        v =dictionary[old_key]
        del dictionary[old_key]
        dictionary[new_key] = v
    else:
        dictionary[new_key] = value
    return dictionary

def read_from_file(directory:str,filename:str):
    if len(directory) != 0:
            directory = directory + '/'
    filename_path = resource_path(os.path.normpath('{0}{1}'.format(directory,filename)))
    try:
        file = open(filename_path)
        result = file.read()
        file.close()
        return result
    except Exception as e:
        print(e)
        return None

def write_to_file(directory:str,filename:str,data:str):
    if len(directory) != 0:
            directory = directory + '/'
    filename_path = resource_path(os.path.normpath('{0}{1}'.format(directory,filename)))
    try:
        file = open(filename_path,'x')
        result = file.write(data)
        file.close()
        return True
    except Exception as e:
        print(e)
        return False

def check_ethereum_types_for_value(value,type,output='check'):
    if type == 'uint256':
        if output == 'check': return check_if_int(value) 
        else: return int(value) 
    elif type == 'address':
        if output == 'check': return Web3.isAddress(value)
        else: return Web3.toChecksumAddress(value) 
    elif type == 'address[]':
        for idx,v in enumerate(value):
            if output == 'check' and not Web3.isAddress(v):
                return False
            elif Web3.isAddress(v):  
                value[idx] = Web3.toChecksumAddress(v)
    if output == 'check':
        return True
    else:
        return value
    
def flatten_list(l:list):
    output = []
    for item in l:
        if isinstance(item,list):
            for sub_item in item:
                output.append(sub_item)
        else:
            output.append(item)
    return output

def check_if_float(potential_float):
    if potential_float == None:
        return False
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def check_if_int(potential_int):
    if potential_int == None:
        return False
    try:
        int(potential_int)
        return True
    except ValueError:
        return False

def check_if_has_key_or_key_is_none(d:dict,key:str):
    if key in d:
        if d[key] != None:
            return True
    return False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..'))
    return os.path.join(base_path, relative_path)

def nvl(value,default):
    '''
    utils helper method: function like the ORACLE SQL NVL-Function

    Parameters
    --------
    value 
        value to check
    default
        output if value is None
    
    Results
    --------
    value or default if value is None
    '''
    if value == None:
        return default
    return value

def add_leading_zeros_to_int(i:int,length:int):
    '''
    utils helper method: add leading zeros to an integer

    Parameters
    --------
    i : int 
        value to check
    length: int
        length of the output string
    
    Results
    --------
    str
        (Default None) a string with leading zeros followed by the input integer i
    '''
    number_length = len(str(i))
    if number_length > length:
        return None
    
    return '{0}{1}'.format((length-number_length)*'0',str(i))


def get_value_from_dict_or_default(dictionary,key:str,default):
    '''
    utils helper method: 

    Parameters
    --------
    dictionary
        dictionary to get value from key. If not a dictionary, default is returned
    key: str
        key of dictionary
    default
        default output when key not in dictionary
    
    Results
    --------
    Value from dictionary or input value default
    '''
    if not isinstance(dictionary,dict):
        return default
    if key == None:
        return default
    if key in dictionary:
        return dictionary[key]
    return default

def rotate_list(l:list,n:int=1):
    '''
    utils helper method: rotate a list l n times

    Parameters
    --------
    l : list 
        dictionary to get value from key
    n: int
        (Default: 1) if n ist positive, rotate n time from left to right. If negative, rotate n times from right to left
    
    Results
    --------
    list
        rotatet list
    '''
    deque_list = deque(l)
    deque_list.rotate(n)
    return list(deque_list)

def dict_key_has_value(dictionary:dict,key:str,value):
    '''
    utils helper method: check is dictionary has value. 

    Parameters
    --------
    dictionary : dict 
        dictionary to check key has value
    key: str
        key name
    value : any
        value of key
    Results
    --------
    bool
    '''
    if dictionary == None:
        return False
    if key in dictionary:
        if dictionary[key] == value:
            return True
    return False

def get_duration(now:datetime.datetime,then:datetime.datetime, interval = "default"):
    '''
    utils helper method: get time difference between two datetimes

    Parameters
    --------
    now : datetime 
        datetime of now
    then: datetime
        datetime of then
    interval : str
        (Default: default) in default mode, you get a string with the time difference. For values in "years","days","hours","minutes","seconds" you get the pure value
    Results
    --------
    str | int
        time difference string or number of time difference interval
    '''
    if then > now:
        duration = then - now # For build-in functions
    else: 
        duration = now -then
    duration_in_s = duration.total_seconds() 
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s
    
    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])
        
        res = []
        if int(y[0]) > 0:
            res.append('{} years'.format(int(y[0])))
        if int(d[0]) > 0:
            res.append('{} days'.format(int(d[0])))
        if int(h[0]) > 0:
            res.append('{} hours'.format(int(h[0])))
        if int(m[0]) > 0:
            res.append('{} minutes'.format(int(m[0])))
        if int(s[0]) > 0:
            res.append('{} seconds'.format(int(s[0])))
        
        return ', '.join(res)

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]

def map_function_input_names_to_value(abi:str,function:str,function_args:list):
    abi = json.loads(abi)
    for a in abi:
        if get_value_from_dict_or_default(a,'type',None) == 'function' and check_if_has_key_or_key_is_none(a,'inputs'):
            if a['name'] == function:
                for idx,i in enumerate(a['inputs']):
                    function_args[idx] = {i['name']: {'value': function_args[idx],'type': i['type']}}
    return function_args

def get_function_from_abi(abi:str=None,function_name:str=None):
    if abi == None or function_name == None:
        return None
    abi = json.loads(abi)
    for a in abi:
        if get_value_from_dict_or_default(a,'type',None) == 'function' and 'name' in a:
            if a['name'] == function_name:
                return a
    return None

def not_flag(flag:str):
    '''
    utils helper method: returns opposite flag value

    Parameters
    --------
    flag : str 
        'Y' or 'N'

    Results
    --------
    'Y' or 'N'; None if flag intput not 'Y' or 'N'
    '''
    if flag == 'Y':
        return 'N'
    elif flag == 'N':
        return 'Y'
    else:
        return None        

def add_pandas_df_column(df:DataFrame,column_name:str,function_on_row,function_args:list=[]):
    df[column_name] = df.apply(lambda row: function_on_row(row,*function_args), axis=1)