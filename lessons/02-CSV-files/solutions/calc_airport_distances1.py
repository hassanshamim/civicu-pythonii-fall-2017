def calc_airport_distances():
    # define two empty dicts that will hold our lat/long info
    airport_lats = {}
    airport_longs = {}

    with open("airports.csv") as airports_csv:
        airport_reader = csv.reader(airports_csv)

        for row in airport_reader:
            airport_lats[row[0]] = float(row[6])
            airport_longs[row[0]] = float(row[7])
            
    return airport_lats, airport_longs
