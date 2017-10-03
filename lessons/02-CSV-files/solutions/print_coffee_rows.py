import csv
def csv_coffee():
    with open("coffee.csv") as coffee_csv:
        my_reader = csv.reader(coffee_csv)

        for row in my_reader:
            print(row)
