import pandas as pd
import string
import numpy as np
import os
import re

doc="""
District to Ubigeo Converter

Input: Inei data on Ubigeos
Output: Panda/Csv with District (Concatenated with Province and Department info) and Ubigeo Columns
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


ubigeos_unfiltered = pd.read_excel('ubigeo_inei.xls', skiprows=1)

# Concatenating departaments, provinces and districts
ubigeos_unfiltered['UBIGEO_DIST_DEP'] = ubigeos_unfiltered['DEPARTAMENTO'].str[:2] + \
    ubigeos_unfiltered['PROVINCIA'].str[:2] + \
    ubigeos_unfiltered['DISTRITO'].str[:2]

ubigeos_unfiltered['DISTRITO'] = ubigeos_unfiltered['DISTRITO'].str[3:]
ubigeos_unfiltered['PROVINCIA'] = ubigeos_unfiltered['PROVINCIA'].str[3:]
ubigeos_unfiltered['DEPARTAMENTO'] = ubigeos_unfiltered['DEPARTAMENTO'].str[3:]

ubigeos_unfiltered['DISTRITO_FULL'] = ubigeos_unfiltered['DISTRITO'] + ", " + \
    ubigeos_unfiltered['PROVINCIA'] + ", " + ubigeos_unfiltered['DEPARTAMENTO']

# Creating a dictionary with ubigeos
distritos = set(list(
    ubigeos_unfiltered['DISTRITO_FULL'].str.strip() + "-" + ubigeos_unfiltered['UBIGEO_DIST_DEP'].str.strip()))
distritos = list(filter(lambda x: str(x) != 'nan', distritos))

for i in range(len(distritos)):
    distritos[i] = distritos[i].split('-')
    distritos[i][0] = normalize(distritos[i][0])

for item in distritos:
    if item[1] == 'DEPRDI':
        distritos.remove(item)

# Creating a list with all the items that don't have full data for erasing them from our main list
distritos_full = []
for item in distritos:
    if len(item[1]) == 6:
        distritos_full.append(item)

# Replacing the original districts values with only the ones that have full data
distritos = distritos_full

dist_names = []
dist_cods = []
for i in range(len(distritos)):
    dist_names.append(distritos[i][0])
    dist_cods.append(distritos[i][1])

df = pd.DataFrame(list(zip(dist_names, dist_cods)),
                  columns=['Name', 'val'])

df.to_excel('dist_ubigeos.xlsx', index=False)
