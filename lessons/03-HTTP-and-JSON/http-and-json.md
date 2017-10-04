# HTTP

- Formed from a request/response cycle
- Client (i.e. your browser) issues a **request** 
- Server (i.e. google.com) recieves the request, processes it, and issues a **response**

This is the request-response cycle.

For now, you should know that requests have a **METHOD**, today we'll be using **GET**, which simply retrieves information.  

Responses have a **status code**, which describes the status of the response.  (200 OK, 404 Not found, 503 service unavailable).  For GET requests, we want to see a status code of  **200**



See:

-  [Anatomy of a request](https://www.tutorialspoint.com/http/http_requests.htm), 
- [HTTP Response Status Codes](https://www.tutorialspoint.com/http/http_status_codes.htm)



## REST URL conventions

We will learn more about REST and its design when we start building our own APIs.  For now, a little context on URL structure may be helpful.



REST APIs are broken down by **resources**.  I.e. `/planets/` `/cart/`, `/products/` etc.

|  Name  |                      Example | Format       |                 Purpose                  |
| :----: | ---------------------------: | ------------ | :--------------------------------------: |
| Index  |  https://swapi.co/api/films/ | /resource/   | Get a list of all objects of that resource.  I.e. Get all Films |
| Detail | https://swapi.co/api/films/2 | /resource/id | Get details of a resource object with the unique identifier `id`.  I.e. Get film with ID 2 |





## Query Parameters

Additional or optional data to send to the web server can be encoded in the url in the form of query parameters.  Query parameters are Key: Value pairs (like in a dictionary) that are added at the end of the URL, following a `?`.  

The URL:

`https://www.reddit.com/r/Python/search?q=example&restrict_sr=on&sort=relevance&t=all`

Has the query parameters:

|     Key     |   Value   |
| :---------: | :-------: |
|      q      |  example  |
| restrict_sr |    on     |
|    sort     | relevance |
|      t      |    all    |



**Note:** the python `requests` library will automatically create this query string  for you if you pass in a dictionary along with your GET request.



## JSON Module

**JSON** ( Javascript Object Notation) is a simple data format which is *extremely* popular with APIs. 

The [Official Specification](http://www.json.org/) can be read, but it's essentially a python dictionary or list that can contain dictionaries,  lists, strings, numbers, and boolean values.

Python comes with the [json module](https://docs.python.org/3/library/json.html) built in.  The two most common functions in the `json` module you may use are:

`json.dumps` - Takes a python dictionary and converts it to JSON.

i.e.

```python
import json
data = {'a': 1, 'b': [1, 2, 3], 'c': 'cat'}
result = json.dumps(data) # convert python data to json
print(result)  # '{"a": 1, "b": [1, 2, 3], "c": "cat"}'
type(result) # str

```



`json.loads` - Takes a json string and converts it to a python dictionary

```python
import json
json_data = '{"a": 1, "b": [1, 2, 3], "c": "cat"}'
result = json.loads(json_data) # converts json to python data
print(result) # {'a': 1, 'b': [1, 2, 3], 'c': 'cat'}
type(result) # dict
```



The json module also comes with `json.load` and `json.dump` which does the same as above but takes a **file object** as an argument.  This is useful if you want to write or read json directly from a file.