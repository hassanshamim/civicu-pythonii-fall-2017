#
""" This module gets information from the petfinder.com API """
#

import requests
import csv
from pprint import pprint as pp

dog_params = {"key":"900cf5ac938676646decc123b24ab678", "animal":"dog", "format":"json"}

def request(req_url, params={}, print_status=False):
    """Makes a request, prints the request status code, and then returns the response"""
    response = requests.get(req_url, params)
    if (print_status): print("...response for <{}> was {}...".format(response.url, response.status_code),flush=True)
    return response

def get_breed_list():
    params = dog_params.copy()
    response = request("http://api.petfinder.com/breed.list", params)
    breed_data_list = response.json()["petfinder"]["breeds"]["breed"]
    breeds = []
    for breed in breed_data_list:
        breed_name = breed["$t"]
        breeds.append(breed_name)
    return breeds
 

#
# begin main
#

breeds = get_breed_list()

req_breed = input("Input dog breed =>")
find_breed = None

for breed in breeds:
    if breed.lower() == req_breed.lower():
        find_breed = breed

if (find_breed == None):
    print ("ERROR ** Unknown breed {} **".format(req_breed))
    print ("Know breeds are listed below:")
    print (breeds)
    exit()

zip_code = input("Enter the starting zip code:")

params = dog_params.copy()
params["breed"]=find_breed
params["location"]=zip_code
response = request("http://api.petfinder.com/pet.find", params)

pets = response.json()["petfinder"]["pets"]["pet"]
print("Found {} {} dogs near {}".format(len(pets), find_breed, zip_code))

for pet in pets:
    name = pet["name"]["$t"]
    city = pet["contact"]["city"]["$t"]
    state = pet["contact"]["state"]["$t"]
    print("{} - {}, {}".format(name, city, state))

