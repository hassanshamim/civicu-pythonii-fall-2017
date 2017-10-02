
## Basics of reading and writing to CSVs

- [links to CSV docs](https://docs.python.org/3/library/csv.html)
- [open() func docs - section on available flags](https://docs.python.org/3/library/functions.html#open)

Today we'll be focusing mainly on using the csv `reader` and `writer`. These tools help us when needing to parse csv files and will serve as a quick and easy way to store data we might want to collect. Below you'll find examples of using a csv reader and writer.

### Reading a File


```python
# Printing a file line by line
with open('example_file.txt') as example:
    for line in example:
        print(line)
        
```

Same as above, without using a [context manager](https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/)


```python
example = open('example_file.txt')
for line in example:
    print(line)
example.close() # context manager does this automatically for us.
```

### CSV reader and writer

```python
import csv

# reader example
with open("foo.csv") as foo: 
    foo_reader = csv.reader(foo)
    
    # this is how you can grab the first header row out of a csv
    header_row = next(foo_reader)
    
    for row in foo_reader:
        print(row)
   
    
# writer example 
with open("foo_write.csv", "w") as foo:
    foo_writer = csv.writer(foo)
    foo_writer.writerow(("col val 1", "col val 2", "col val 3", "col val 4"))
    
```

We'll get more familiar with csvs by using an exercise provided by `OpenTechSchool`. You can find the link to the exercise [here](http://opentechschool.github.io/python-data-intro/core/csv.html). Before starting this exercise please read the notes below about the changes/modifications that have been made to suit the needs of our class.

## Explanation of challenges in the `OpenTechSchool` exercise

In the sections below we'll walk through each of the pieces of the exercise linked above. Note that we're not going to be working on the last section of the provided challenge where we're asked to plot the results of the distance calculation.

### Coffee csv challenge

In this exercise our task is to open the coffee csv, loop over its rows, and print each row. This is useful because it is the basic pattern we will follow anytime that we want to access data that is being stored in a csv. 

**HINT**: look at the `reader example` above to use as a template.


```python
%load solutions/print_coffee_rows.py
```

Notice how we define a reader object that then lets us loop through each row that is inside of the coffee.csv file. Remember that when looping through the rows in a csv the values in each row will be given to you as a list of strings

### Reading airport data challenge

In this part of the challenge we are looking at the `airports.csv` file and are tasked with printing out only the rows for airports that are in a specific country. You can pick any country you like for this challenge. 


```python
%load solutions/airports_of_canada.py
```

In the solution above we're opening a csv.reader object so we're then able to loop through the rows contained in the `airport.csv`.

```python
# airport.csv Headers
['ID', 'Airport-Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz-Type', 'Source']
```

Just like all rows that we get back from the csv reader the header row is a list of strings. The header row let us know what the values in each column of the csv mean. For this challenge we're looking for the country that an airport is from so we know that we need to check the value at the 3rd index when we're looping through each row in the csv.

We then loop through each row using a for loop and check to see if the value in the 3rd index is equal to `"Canada"`. If the airport is from Canada we then print out the row.

As an extra challenge try to change this function so that you can pass in an argument that is a country's name and then only print the rows that have an airport from that country

### Calculating the distances between two airports

In this part of the challenge we were asked to calculate the distance for all of the airline routes in the `routes.csv`. In order to solve this part of the challenge we need to combine data that we have in two different files to get the correct information to perform this task. 

We are given a `geo_distance` function seen below to help us with this calculation.


```python
%load geo_distance.py
```

It's not necessary to understand the equation being used in this function in order for us to be able to use it to calculate the distance between two points. If we look at the function we can see that it takes four arguments, two pairs of lat/long coordinates.

In order to solve this challenge we need to pass in the lat/long coordinates for each set of airports found in the rows of the routes.csv. 

The problem is all of our lat/long information is stored in the airports.csv and is only stored once per airport. This is a common pattern when storing information about items that relate to one another. In this case each individual airport could have potentially dozens of routes (rows in the routes.csv) leaving to and from it daily. If we were to store the lat/long for each airport in every row in the routes.csv we would be writing down a ton of repetitive information and would make the file much larger than it needs to be. Instead the csv is setup to use the unique id for each airport when they need to describe any relationship between airports. Doing this lets us model the relationship between two airports without having to write down a bunch of extra information about each airport on every row of the routes.csv.

If we want to calculate the distance between two airports it's up to us to look up the pieces of information we need from the `airport.csv` so we can then use that information when we're looping through the `routes.csv`.

In the examples below we'll walk through the process of building up the lat/long information we need.


```python
%load solutions/calc_airport_distances1.py
```

In the code above we define two empty dicts and then loop through each row in the `airports.csv` grabbing the `id` at the 0th index and then the lat or long depending on which dictionary we're adding the information to. Remember that the `id` for an airport is the same in both the `airports.csv` and the `routes.csv`

By doing this we're building a lookup dictionary that we can use later when we loop through the `routes.csv` and need the lat/long for each airport. Notice that we're also converting the `string` values to `float` with the lat/longs so that we can use them in the `geo_distance` function later.

Now that we have two dictionaries that contain the lat and long for each airport we're ready to loop through the `routes.csv`. 

In order to know which indexes we need values from in the `routes.csv` it's helpful to look at the headers. See below


```python
# route.csv headers
['Airline', 'Airline-ID', 'Source-airport', 'Source-airport-ID', 'Destination-airport', 'Destination-airport-ID', 'Codeshare', 'Stops', 'Equipment']
```

Looking at the headers we can see that we want to lookup the `Source-airport-ID` (the 3rd index) and the `Destination-airport-ID` (the 5th index). The ids in these positions will match the ids from the airports in the `airports.csv` and will give us a way to look up the lat/long information we need using the dictionaries we created above.

Below I've included the code that opens the `routes.csv`. Notice how we do this in the same function where we're building out lookup dictionaries. We could have these as two separate functions but it makes it easier to keep everything in one place for the moment.


```python
%load solutions/calc_airport_distances2.py
```

At this point if you run the code above it will build the lookup dicts we need for the lat/long values by opening the `airports.csv`. Then it will open the `routes.csv` and loop through each row grabbing the source and destination airport ids from each set of airports. It then checks that the source and destination airport ids are in the lat/long dicts and if they are it grabs the lat/long pairs for each airport. With these coordinate pairs we're then able to pass them into the `distance` function and calculate the distance between the airports for each row in the `routes.csv`. 

With the code above we're calculating the distance value but not saving it anywhere, in each loop we calculate the kilometer distance between the two airports but then throw that value away. If we wanted to save this calculation so that we could use it later on in a different program we could write it to a new csv. Look at the code below and see how we're able to open a csv to write our information to while we're looping through the `routes.csv


```python
%load solutions/calc_airport_distances3.py
```

While the code above is not the most efficient way to write to the new `dist_info.csv` because we're repeatedly opening and closing it every time we loop through a row of the `routes.csv` it gives us a quick example of how you can save information to a file. If you run the code above you'll see a new `dist_info.csv` file created in the directory you're in. By using the `a` flag when we open the file we're saying that we want to append information to it and not overwrite what is already there. If you were to use `w` instead of `a` you would end up with only one row in your newly created file because it would erase the file every time we opened it inside the loop.

### Ideas for further challenges

Now that we have seen a rough way to solve this problem I would like everyone to try to modify the code above in some way. Below you'll find ideas of possible side projects. These aren't required but would be a useful way to get extra practice. 

- Adjust the final function to only open the output csv file *once* and write all the data to it.
- Count the number of airports in each country.  Write your results to a new csv file.
- Find the longest flight in routes.csv  What is the airport codes (NOT id) of the source and destination?
- Try to write more information than just the `source_id`, `dest_id`, and `km_dist` to the final csv. (remember that when using the `a` flag no information is erased, so multiple runs of the function above will keep adding rows) 
- Try to rework how the code is organized so instead of having one large function that does everything, break the steps needed to solve this problem into smaller pieces contained in separate functions.
- Rework the way data is stored in the above examples by storing airport `lat` and `long` together, rather than in separate dictionaries.  You may have to change the function header of the `distance` function.  **Optional**: see if [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple) would be useful.
- Add a header row (column names, as found in the OpenFlight data webpage) to the csv files.  Rewrite the examples (or one of the above challenges) to use [csv.DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader)
- Find other interesting csv data that is openly available and see if you can pull out the pieces that interest you and write them to a new csv using the techniques described above.



### Useful ways to inspect files

There are a few useful commands if you're on a linux/unix os that can help you inspect the csv files you're creating. The commands are listed below with a brief description of what they do. [Link to stackoverflow question about using tail command on windows](https://stackoverflow.com/questions/1295068/windows-equivalent-of-the-tail-command)

- `tail <file_name>` - This will show you the last 10 lines of a file in the terminal
- `head <file_name>` - This will show you the first 10 lines of a file in the terminal
  - with both commands above you can pass additional flags to them that cause different outputs. One useful flag is the `-f` flag. This flag will let you follow what is happening to the file so if you have a long running write you can visually check that the file is getting written to. [Link to other flags](https://www.linux.com/blog/14-tail-and-head-commands-linuxunix)
- `wc -l *` - If you run this command in a directory with your csv files if will count the lines in each one. It's a useful way to spot check files and make sure that you go the correct number of rows you were expecting.

