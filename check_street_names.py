# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:34:38 2017

@author: kasalit
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script is used to check street names - to check for correctness.
## I added 2 functions to check for city names as well.

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("map", "r")

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
city_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)
city_types = defaultdict(int)


## Uses reqular expressions to check the street names 
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1


## Uses reqular expressions to check the city names 


def audit_city_type(city_types, city_name):
    m = city_type_re.search(city_name)
    if m:
        city_type = m.group()

        city_types[city_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 
        
        
### Returns true if the tag element is Street
def is_street_name(elem):
     return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")
     ##return (elem.tag == "tag") and (elem.attrib['k'] == "bridge")
     ##return (elem.tag == "tag") and (elem.attrib['k'] == "highway")

### Returns true if the tag element is City   
def is_city_name(elem):
     return (elem.tag == "tag") and (elem.attrib['k'] == "addr:city")
     
     
     
def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)  
    
def audit_c():
    for event, elem in ET.iterparse(osm_file):
        if is_city_name(elem):
            audit_city_type(city_types, elem.attrib['v'])    
    print_sorted_dict(city_types)

if __name__ == '__main__':
    audit_c()