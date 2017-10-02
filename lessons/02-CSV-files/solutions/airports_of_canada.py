def csv_airport():
    with open("airports.csv") as airports_csv:
        airport_reader = csv.reader(airports_csv)

        for row in airport_reader:
            if row[3] == "Canada":
                print(row)
