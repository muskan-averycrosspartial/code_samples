#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:54:11 2022

@author: muskanaggarwal
"""

import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.census2011.co.in/district.php"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


print(page.text)



table = soup.find(id="table1")


#table1 > div > table > tbody > tr:nth-child(1) > td:nth-child(4)

table_rows = table.find_all("tr")
all_elements = ""

for row in table_rows:
    element = row.text
    element = element.strip('\n')
    element = re.sub(r',', '', element )
    element = re.sub(r'\n', ',', element )
    element = re.sub(r'%', '', element )
    #element = re.sub(r' ', '', element )
    element = element.lower()
    element = element + '\n'
    all_elements = all_elements + element
    
with open('processed_data/scraped_census.csv', 'w', newline='\n') as ofile:
    ofile.write(all_elements)


