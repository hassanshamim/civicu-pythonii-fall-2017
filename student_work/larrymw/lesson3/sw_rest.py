#
""" This module gets information from swapi.com and writes it to a CSV file """
#

import requests
import csv
from pprint import pprint as pp

def request(req_url):
    """Makes a request, prints the request status code, and then returns the response"""
    response = requests.get(req_url)
    print("...response for <{}> was {}...".format(req_url, response.status_code),flush=True)
    return response

def get_planet (planet_number):
    """Returns the json dict for the specified plant number"""
    presponse = request("http://swapi.co/api/planets/" + str(planet_number))
    return presponse.json()

#
# begin module main
#

# Data will be written to this file
output_filename = "residents.csv"

# Get the info about planet 1
p1_dict = get_planet(1)

# Begin the list of data that will be written to the output file
resident_data = [p1_dict["name"], p1_dict["url"] ]

#
# Get the url for each resident, fetch the resident info, and add it to the output list
for purl in p1_dict['residents']:
    resident_dict = request(purl).json()
    resident_data.append(resident_dict["name"])

print ("Writing following data to file <{}> :".format(output_filename))
pp(resident_data)

# Write the output list a file as CSV
with open(output_filename, "w") as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(resident_data)

print ("!!! Complete !!!")


