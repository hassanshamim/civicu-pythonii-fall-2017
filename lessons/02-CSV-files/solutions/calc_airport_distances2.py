def calc_airport_distances():
    # define two empty dicts that will hold our lat/long info
    airport_lats = {}
    airport_longs = {}

    with open("airports.csv") as airports_csv:
        # setup reader and remove header
        airport_reader = csv.reader(airports_csv)

        for row in airport_reader:
            airport_lats[row[0]] = float(row[6])
            airport_longs[row[0]] = float(row[7])
            
    # now that we have lookup dicts for lat/long loop through the routes 
    with open("routes.csv") as routes_csv:
        route_reader = csv.reader(routes_csv)

        for row in route_reader:
            source_id = row[3]
            dest_id = row[5]

            # check to see if the ids for both airports are in the lookup dicts
            if source_id in airport_lats and dest_id in airport_lats:
                # use the lat/long dicts to get the coordinate info for each airport
                source_lat = airport_lats[source_id]
                source_long = airport_longs[source_id]
                dest_lat = airport_lats[dest_id]
                dest_long = airport_longs[dest_id]
                
                # make a variable that captures the output from the geo_distance function
                km_dist = geo_distance.distance(source_lat,
                                                source_long,
                                                dest_lat,
                                                dest_lat)
