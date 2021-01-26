#
""" This module finds dogs for adoption """
#

import requests
import csv
from pprint import pprint as pp

# The standard parameters that petfinder.com uses for all dog requests
dog_params = {"key":"900cf5ac938676646decc123b24ab678", "animal":"dog", "format":"json"}

def request(req_url, params={}, print_status=False):
    """Makes a request, optionally prints the request status code, and then returns the response"""
    response = requests.get(req_url, params)
    if (print_status): print("...response for <{}> was {}...".format(response.url, response.status_code),flush=True)
    return response

def get_breed_list():
    """ Gets a list of petfinder.com known dog breeds """

    # request a list of all dog breeds
    response = request("http://api.petfinder.com/breed.list", dog_params)

    # dig into the returned data to find a list of breed entries
    breed_data_list = response.json()["petfinder"]["breeds"]["breed"]

    # this will hold the list of breed names
    breeds = []

    # extract the breed name for each entry and add it to the list
    for breed in breed_data_list:
        breed_name = breed["$t"]
        breeds.append(breed_name)

    # return the list of known breeds
    return breeds

def find_dogs(breed, zipcode):
    """ Find adoptable dogs of the given breed near the given zipcode """

    # add the dog breed and zipcode to the standard dog query parameters
    params = dog_params.copy()
    params["breed"]=breed
    params["location"]=zip_code

    # query the petfinder.com API and return the list of pets found
    response = request("http://api.petfinder.com/pet.find", params)
    return response.json()["petfinder"]["pets"]["pet"]

def get_zipcode_city(zipcode):
    """ Uses zippopotaums API to find the city associated with the given ZIP code """

    # query the Google maps api for information on the given zipcode
    response = request("https://api.zippopotam.us/us/"+zipcode)

    # make sure the request was successful
    if (response.status_code < 200 or response.status_code > 299): return None

    response_data = response.json()
    place = response_data["places"][0]

    # return the city name from the response information
    return "{}, {} {}".format(place["place name"], place["state abbreviation"], response_data["post code"])

#
# begin main
#

print ("<< This program will help you find adoptable dogs by breed and location >>")

# Get the list of known breeds
breeds = get_breed_list()

# Ask the user for their requested breed
req_breed = input("Input dog breed =>")

#
# Compare the user's requested breed with the list of known breeds.
# If a case insenstive comparison matches, then use the breed name from the list
#  
find_breed = None
for breed in breeds:
    if breed.lower() == req_breed.lower():
        find_breed = breed

# If find_breed is undefined then we didn't find the users breed in the known breed list
if (find_breed == None):
    print ("ERROR ** Unknown breed {} **".format(req_breed))
    print ("Known breeds are listed below:")
    print (breeds)
    exit()

# Get the zip code where the search should begin
zip_code = input("Enter the starting zip code:")

# Get the city associated with the requested ZIP code
search_city = get_zipcode_city(zip_code)

# If the city wasn't found, then the ZIP code was invalid
if search_city == None:
    print("ERROR ** Unknown ZIP code {} **".format(zip_code))
    exit()

# Let the user send the pet information to an output file
output_filename = input("Enter output file name (Hit <enter> for no file output) =>")

print ("Searching for {} dogs near {}...".format(find_breed, search_city))

# Find the matching dogs
pets = find_dogs(find_breed, zip_code)

# This will hold a list of found pets
found_pets = []

#
# For each pet in the JSON data, pick out the name, city and state
# Write this to the console and also save it in a list
#
for pet in pets:
    name = pet["name"]["$t"]
    city = pet["contact"]["city"]["$t"]
    state = pet["contact"]["state"]["$t"]
    found_pets.append({"name": name, "city": city, "state": state})
    print("{} - {}, {}".format(name, city, state))

print("Found {} {} dogs near {}".format(len(pets), find_breed, search_city))


# If an output file was specified by the user, write the pet information to
# the file as CSV

if output_filename != "":
    with open(output_filename, "w") as outfile:
        writer = csv.DictWriter(outfile, ["name", "city", "state"])
        writer.writeheader()
        for pet in found_pets:
            writer.writerow(pet)
    print ("Pet information written to file <{}>".format(output_filename))




