# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 11:44:14 2017

@author: kasalit
"""
import cleaning
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
city_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


map_city = { "lagos": "Lagos",
            "Lagaos": "Lagos"
            }

## Mapping dictionary to update street names

mapping = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "road.": "Road",
            "Ave.": "Avenue",
            "Ave" : "Avenue",
            "close": "Close",
            "Cres": "Crescent",
            "kirikiri": "Kirikiri Road",
            "Thomas": "Thomas Street"
            }


## Audit the keys for each tag to get the key type
def audit_keys(test):
    """ audit the keys for each tag to get the key type
    
    Args:
        test : takes the key value that is tested
        
    Returns:
        Returns the type of key as either Regular or the second part of the key if seperated by a colon:
    
    """ 
    val_key = ''
    val_type = ''
    LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
    LOWER_COLON_3 = re.compile(r'^([a-z]|_)+:([a-z]|_)+:([a-z]|_)+')
    PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    
    m = PROBLEMCHARS.search(test)
    t = LOWER_COLON_3.match(test)
    u = LOWER_COLON.match(test)
    
    if m:
       val_key = None
       val_type = None
    elif t:
          values = t.group()
          #print values
          clean_val = values.split(':',1)
          val_type = clean_val[0]
          val_key = clean_val[1]
          #print val_type
         # print val_key
          
    elif u:
          values = u.group()
          #print values
          clean_val = values.split(':',1)
          val_type = clean_val[0]
          val_key = clean_val[1]
          #print val_type
          #print val_key
    else:
        val_key = test
        val_type = 'regular'
        
    return val_key, val_type
    
    

### Returns true if the tag element is Street
def is_street_name(elem):
    """     
    Args:
        elem : takes an element as an argument
        
    Returns:
        Returns true if the element atrribute is "addr:street"
    
    """ 
    return (elem.attrib['k'] == "addr:street")

### Returns true if the tag element is city
  
def is_city_name(elem):
    """     
    Args:
       elem : takes an element as an argument
        
     eturns:
       Returns true if the element atrribute is "addr:city"
    """
    return (elem.attrib['k'] == "addr:city")


def is_postcode(elem):
    """     
    Args:
       elem : takes an element as an argument
        
     eturns:
       Returns true if the element atrribute is "addr:postcode"
    """
    return (elem.attrib['k'] == "addr:postcode")
    
    
## function to update the street name using the mapping dictonary.  
    
def update_name(name, mapping):
    """     
    Args:
       name : The value of the street key
       mapping: Mapping of old street names to corrected streetnames
        
    Returns:
       
       returns the updated streetname if a mapping exists.
       
     """
    
    t = street_type_re.search(name)
    if t:
        st_name = t.group()
        if mapping.has_key(st_name):
           new_name = mapping[st_name]
           return name.replace(st_name,new_name)
        else:
            return name
    else:
        return name
            
## function to update the city name using the mapping dictonary.
            
            
def update_city(name, map_city):
    """     
    Args:
       name : The value of the city  key
       mapping: Mapping of old city names to corrected city names
        
    Returns:
       
       returns the updated city name if a mapping exists.
       
     """
    
    l = city_type_re.search(name)
    if  l:
        ct_type = l.group()
        if map_city.has_key(ct_type):
           new_name = map_city[ct_type]
           return name.replace(ct_type,new_name)
        else:
            return name
    else:
        return name
     


def update_postcodes(postcode):
    
    """     
    Args:
       postcode : The post code Value
       
        
    Returns:
       
       returns the original post code if it's matches the expected format, else changesthe value to None.
       
     """
      
    m = re.match(r'^\d{6}$', postcode)
    if not m:
           return None
           
    else:
          return postcode
    