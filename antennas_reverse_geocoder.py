import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

doc="""
Reverse Geocoder for Mobile Phone Antennas in Peru

input: csv with coords of each antenna
output: new csv with 2 extra columns containing the district and ubigeo of each antenna
"""

# Importing our database of peruvian phone antennas
antennas = pd.read_csv('u_antennas.csv')

# Creating our new address an ubigeo columns
antennas['address'] = ''
antennas['ubigeo'] = ''

# Defining a reverse geocoder function
def reverse_geo(coordinates, dataframe, row_index, attempt=1, max_attemps=5):
    """
    The purpose of this function is mainly to do reverse geocoding of our coordinates,
    but also to avoid the `geopy.exc.GeocoderTimedOut: Service timed out` error
    """
    try:
        # Calling our Free Geocoder
        locator = Nominatim(user_agent='myGeocoder')
        # Obtaining the address of our antennas
        location = locator.reverse(coordinates)
        dataframe.iloc[row_index, 3] = location.address
    except GeocoderTimedOut:
        if attempt <= max_attemps:
            return reverse_geo(coordinates, dataframe, row_index, attempt=attempt+1)
        raise

# Looping across each row 
counter = 0
for row in range(0, antennas.shape[0]):
    # Coords are 1 for Latitude and 2 for Longitude
    coords = str(antennas.iloc[row][1]) + ", " + str(antennas.iloc[row][2])
    # Calling our reverse geocoder
    reverse_geo(coords, antennas, row)
    counter = counter + 1
    print("# of completed iterations: " + str(counter))

print(antennas.head())
# Saving our data
antennas.to_csv('antennas_adresses.csv', index=False)
