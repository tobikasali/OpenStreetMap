# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:02:42 2017

@author: tobikasali
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "map"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
city_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
post_code_re = re.compile(r'^\d(5)$')
##re.match(r'^\d(5)$', postcode)

## Expected values for street types

expected = ["Street", "Avenue", "Way", "Drive", "Close", "Road", "Crescent"]

## Expected Values for City

expected_city = ["Lagos"]

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
  

## Mapping dictionary to update city  names
          
map_city = { "lagos": "Lagos",
            "Lagaos": "Lagos"
           }


def audit_street_type(street_types, street_name):
    """  
    checks if the steet type matches the any of the expected street types
    if not, add to the dictionary.
    
    Args:
       street_types : Dictionary of street types
       street_name: the value of street key
           
     """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
            
def audit_city_type(city_types, city_name):
    """  
    checks if the city type matches the any of the expected city types
    if not, add to the dictionary.
    
    Args:
       city_types : Dictionary of street types
       city_name: the value of street key
           
     """
    m = city_type_re.search(city_name)
    if m:
        city_type = m.group()
        if city_type not in expected_city:
            city_types[city_type].add(city_name)
            
            
            
def audit_post_codes(code_types, postcode):
    """  
    checks if the post code matches the expected 6 digit format of lagos state postcodes
    if not, add to the dictionary.
    
    Args:
       code_types : Dictionary of list of post codes
       post_code: the value of postcode key
           
     """
    m = re.match(r'^\d{6}$', postcode)
    if not m:
        code_type = postcode
        code_types[code_type].append(postcode)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")
    
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")



def audit(osmfile):
        
    """  
    Audit the street values in the amp
    
    Args:
       osmfile : map file to audit
       
    Returns
    
      Returns the unxepected street types
      
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    
    return street_types


def audit_city(osmfile):
    
    """  
    Audit the city values in the amp
    
    Args:
       osmfile : map file to audit
       
    Returns
    
      Returns the unxepected city types
    """
    osm_file = open(osmfile, "r")
    city_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_type(city_types, tag.attrib['v'])
    osm_file.close()
    
    return city_types
    
    
def audit_postcode(osmfile):
    """  
    Audit the postcode values in the amp
    
    Args:
       osmfile : map file to audit
       
    Returns
      Returns a dictionary of lists of unxepected post codes
    """
    
    osm_file = open(osmfile, "r")
    code_types = defaultdict(list)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    print tag.attrib['v']
                    audit_post_codes(code_types, tag.attrib['v'])
    osm_file.close()
    
    return code_types
    
## function to update the street name using the mapping dictonary.
    
def update_name(name, mapping):
    
    t = street_type_re.search(name)
    if t:
        st_type = t.group()
        if mapping.has_key(st_type):
           new_name = mapping[st_type]
           return name.replace(st_type,new_name)
        else:
            return name
    else:
        return name
        
## function to update the city name using the mapping dictonary.
            
def update_city(name, map_city):
    
    t = city_type_re.search(name)
    if t:
        ct_type = t.group()
        if map_city.has_key(ct_type):
           new_name = map_city[ct_type]
           return name.replace(ct_type,new_name)
        else:
            return name
    else:
        return name
                    

def update_postcodes(postcode):
    
    
    m = re.match(r'^\d{6}$', postcode)
    if not m:
           return None
           
    else:
          return postcode
    
#if __name__ == '__main__':
#    test()

# Working Version
"""
old_name = 'Bode Thomas'
t = street_type_re.search(old_name)
if t:
   st_name = t.group()
   if mapping.has_key(st_name):
      new_name = mapping[st_name]
      print old_name.replace(st_name,new_name)
   else:
      print old_name
else:
    print old_name

"""
"""    
old_name = 'lagos'
t = city_type_re.search(old_name)
if t:
    ct_type = t.group()
    if map_city.has_key(ct_type):
       new_name = map_city[ct_type]
       print old_name.replace(ct_type,new_name)
    else:
       print old_name
else:
     print old_name

"""
"""
postcode = '10281'
m = re.match(r'^\d{6}$', postcode)
if not m:
      print postcode
   
"""  

test = update_postcodes('102811') 

print test


#cool = audit_postcode(OSMFILE)
#pprint.pprint(dict(cool))