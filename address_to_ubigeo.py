import pandas as pd
import string
import numpy as np
import os
import re

doc = """
Address to Ubigeo Converter

Input: Antennas full addresses 
Output: Antennas District Locations and Ubigeo 
"""

# We first define a cleaner for unusual characters
def normalize(s):
    replacements = (
        ("á", "a"),
        ("à", "a"),
        ("é", "e"),
        ("è", "e"),
        ("í", "i"),
        ("ì", "i"),
        ("ó", "o"),
        ("ò", "o"),
        ("ú", "u"),
        ("ù", "u")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

antennas = pd.read_csv('antennas_adresses.csv')

# List of addresses
address = list(antennas['address'].str.strip())
print(address)

# Cleaning the address
for i in range(0, len(address)):
    address[i] = address[i].split(',') 
    # Cleaning all the items of an address
    for j in range(0, len(address[i])):
        address[i][j] = address[i][j].strip()
        address[i][j] = normalize(address[i][j])
    # Erasing all the numeric character items or the ones that include a number
    for item in address[i]:
        if re.match(r'*\d*', item):
            address[i].remove(item)
    # Keeping the last three elements (in theory: District, Province, Department)
    address[i] = address[i][-3]

