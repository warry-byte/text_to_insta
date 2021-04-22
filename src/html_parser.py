# # HTML Parser 

from bs4 import BeautifulSoup
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import dateutil.parser
import locale
import json
import collections

def flatten(x):
    # flatten list of strings
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def remove_text_start(txt):
    i = 0 # pointer to the next 

    for s in txt:
        if(s == '\n' or s == ' '):
            i += 1
        else:
            break
        
    return txt[i:]

def str_to_list(txt):
    # first split according to \n\n. First row will be the quote (which may contain a \n character).
    out_list = []
    list1 = txt.split('\n\n')
    out_list.append(list1[0])
    # first row will now be the quote
    # split subsequent 
    for s in list1[1].split('\n'):
        out_list.append(s)
        
    out_list = flatten(out_list)
    out_list = [a for a in out_list if a != ''] # remove empty list items
    
    return out_list

def convert_date_text(date_txt):
    # Format of input: ' January 5th, 2014 11:01am '
    # Output: 'Dimanche 05 janvier 2014'
    try:
        date_obj = dateutil.parser.parse(date_txt) 
    except:
        print(date_txt)
        
    locales = ['fr']
    loc = locales[0]
    locale.setlocale(locale.LC_ALL, loc) # change to French
    output_date = date_obj.strftime("%A %d %B %Y").capitalize()
    
    return output_date

def cleanup_str_list(str_list):
    # Expected format: 
    # ['Ça commence par un front, et ça termine par un cul.                    — ',
    # ' January 5th, 2014 11:01am ',
    # 'salace',
    # 'boucle infinie',
    # Note: no empty string!

    quote = remove_quote_caca(str_list[0])
    date_txt = convert_date_text(str_list[1])
    # get words in subsequent fields
    hashtags = [word for word in str_list[2:] if word != '']
            
    output = {
        'quote' : quote, 
        'hashtags' : hashtags, 
        'date' : date_txt
        }
    
    return output

def remove_quote_caca(quote):
    # Heuristic to retrieve the quote: look for three consecutive spaces. The quote is located before the three consecutive spaces
    try:
        ind = quote.index('   ')   
        output_quote = quote[:ind]
    except:
        output_quote = quote
        
    return output_quote
    
def write_dict_to_file(quote_dict, filename):
    with open(filename, 'w+') as f:
        # json.dump(quote_dict, f, ensure_ascii=False)
        json.dump(quote_dict, f)

    
def read_dict_from_file(filename):
    with open(filename, 'r') as f:
        file_txt = f.read()
        output_dict = json.loads(file_txt)
        
    return output_dict