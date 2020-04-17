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

# Cleaning the address
for i in range(0, len(address)):
    address[i] = str(address[i]).split(',') 
    # Cleaning all the items of an address
    for j in range(0, len(address[i])):
        address[i][j] = address[i][j].strip()
        address[i][j] = normalize(address[i][j])

for i in range(0, len(address)):
    # degug point: print(address[i])
    aux_list = []
    for item in address[i]:
        if not(re.match(r'^(?=.*\d).+$', item)) and item != 'Peru' and len(item) > 1:
            aux_list.append(item)
    address[i] = aux_list
    # degug point: print(address[i])

dist_ubigeos = pd.read_excel('dist_ubigeos.xlsx')
dist_ubig_list = list(dist_ubigeos['Name'] + ", " + dist_ubigeos['val'].astype('str'))

for antenna in address:
    print("Evaluating antenna located in: " + str(antenna))
    for dist_ubig in dist_ubig_list:
        dist_ubig = dist_ubig.split(',')
        # Erasing unncessary spaces
        dist_ubig = [item.strip(' ') for item in dist_ubig]
        # Matches per antenna: an antenna address should have exactly 3 matches to the elements of one dist_ubig item
        num_matches = 0
        # List with the antennas that matched 2 items of a dist_ubig
        match_2 = []
        for item in antenna:
            # Checking if the items on antenna match any item in dist_ubig
            if item in dist_ubig:
                num_matches += 1
        # To avoid running through all dist_ubig_list elements even when we have found one item that works:
            if num_matches == 2:
                match_2.append(antenna)
            if num_matches == 3:
                # todo: statement for attaching the ubigeo to our antennas list items
                antenna.append(dist_ubig[-1])
                print('The antenna located in ' + str(antenna) +
                      ' was matched with ubigeo ' + str(dist_ubig[-1]))
                break
        print('The items in ' + str(antenna) + ' only matched ' + str(num_matches) + ' items of ' +
                str(dist_ubig))

print('The antennas that matched 2 items were: ' + str(match_2))


