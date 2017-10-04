#
# Calculates the distances of routes between airports
#
# Airport and route data are read in from CSV files and the distance of each route is written to
# the output file "distances.csv" in CSV format
#

import csv
import geo_distance

#
# Given a row of data from the airport data file, return a tuple of (lattitude, longitude)
#
def get_lat_long(airport_file_row):
    return float(airport_file_row["Latitude"]), float(airport_file_row["Longitude"])

#
# Given a source and destination point (lattitude, longitude) tuple, return the distance between the two points
#
def get_distance(source_tuple, dest_tuple):
    return geo_distance.distance(source_tuple[0], source_tuple[1], dest_tuple[0], dest_tuple[1])

#
# Get the data from an airport file. Data is returned as a dictionary in the following format:
# {<ID>:<airport data as dictionary>}
#

def get_airport_data(airport_file_name):
    # This is the date arrangement for each row of the airport data
    airport_file_headers = ['ID', 'Airport-Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz-Type', 'Source']
    airport_data = {}

    #
    # Read each line from the data file and store each airport's data in a dictionary with the
    # airport ID as the key
    #

    with open(airport_file_name, encoding="utf-8") as infile:
        reader = csv.DictReader(infile, airport_file_headers)
        for row in reader:
            airport_data[row['ID']] = row

    return airport_data

### Begin main ###

# Get the airport data from the input file
airport_data = get_airport_data("airports.dat")

# This is the date arrangement for each row of the route data
route_file_headers = ['Airline', 'Airline-ID', 'Source-airport', 'Source-airport-ID', 'Destination-airport', 'Destination-airport-ID', 'Codeshare', 'Stops', 'Equipment']

#
# Read the route file,  calculate the distance for each rout and write the result to the output file
#

with open("routes.dat") as infile, open ("distances.csv", "w") as outfile:
    # Reads the CSV rows of the route file
    reader = csv.DictReader(infile, route_file_headers)

    # Writes the CSV rows of the output file
    writer = csv.DictWriter(outfile, ['Source-airport-ID', "Destination-airport-ID", "Distance"])

    # Write the CSV headers to the output file
    writer.writeheader()

    #
    # Read and process each row in the route file
    #
    for row in reader:

        # Make sure that the source airport id for this route is in our airport data
        source_id = row['Source-airport-ID']
        if (source_id not in airport_data):
            print("** ERROR: Source airport id <{}> is unknown **".format(source_id))
            continue
        source_name = row['Source-airport']

        # Make sure that the destination airport id for this route is in our airport data
        dest_id = row['Destination-airport-ID']
        if (dest_id not in airport_data):
            print("** ERROR: Destination airport id <{}> is unknown **".format(dest_id))
            continue
        dest_name = row['Destination-airport']

        # Calculate the distance between the source and destination airport for this route
        distance = get_distance(get_lat_long(airport_data[source_id]), get_lat_long(airport_data[dest_id]))
        print ("Distance from <{}> to <{}> is {}".format(source_name, dest_name, distance))

        # Write this route information to the output file
        writer.writerow({'Source-airport-ID':source_id, "Destination-airport-ID":dest_id, "Distance":distance})

      