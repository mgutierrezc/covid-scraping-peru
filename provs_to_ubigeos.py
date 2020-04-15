import pandas as pd
import string
import numpy as np
import os
import re

doc = """
Province to Ubigeo Converter

Input: Inei data on Ubigeos
Output: Panda/Csv with Province and Ubigeo Columns
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

# Concatenating departaments and provinces
ubigeos_unfiltered['UBIGEO_PROV_DEP'] = ubigeos_unfiltered['DEPARTAMENTO'].str[:2] + \
    ubigeos_unfiltered['PROVINCIA'].str[:2]

ubigeos_unfiltered['PROVINCIA'] = ubigeos_unfiltered['PROVINCIA'].str[3:]

# Creating a dictionary with ubigeos
provincias = set(list(
    ubigeos_unfiltered['PROVINCIA'].str.strip() + "-" + ubigeos_unfiltered['UBIGEO_PROV_DEP'].str.strip()))
provincias = list(filter(lambda x: str(x) != 'nan', provincias))

for i in range(len(provincias)):
    provincias[i] = provincias[i].split('-')
    provincias[i][0] = normalize(provincias[i][0])

for item in provincias:
    if item[0] == '' or item[0] == 'VINCIA' or len(item[1]) < 3:
        provincias.remove(item)

prov_names = []
prov_cods = []
for i in range(len(provincias)):
    prov_names.append(provincias[i][0])
    prov_cods.append(provincias[i][1])

df = pd.DataFrame(list(zip(prov_names, prov_cods)),
                  columns=['Name', 'val'])

df.to_excel('prov_ubigeos.xlsx', index=False)
