# Django JSON APIs

Code for this Lesson is available under the `django-json-api` branch of [swapi-models](https://github.com/hassanshamim/swapi-models/tree/django-json-api)

- Write a plain JSON API for our `Planet` model using just Django
- Explore the challenges of this process
- Introduce DRF Serializers



REST - A style of designing your APIs (Architecture)
CRUD - common operations against persistent storage (your database)

- **C**reate
- **R**ead / **R**etrieve
- **U**pdate
- **D**elete



How do they map to the REST architecture pattern?



| HTTP verb | Operation | View Name |           URL Example           |
| :-------: | :-------: | :-------: | :-----------------------------: |
|    GET    |   READ    |   List    |  www.example.com/api/planets/   |
|   POST    |  CREATE   |  Create   |  www.example.com/api/planets/   |
|    GET    |   READ    | Retrieve  | www.example.com/api/planets/1/  |
|    PUT    |  UPDATE   |  Update   | www.example.com/api/planets/1/  |
|  DELETE   |  DELETE   |  Destroy  | www.example.com/api/planets//1/ |





# Creating a JSON API for our Models

So far we have learned to create and query our models from the database.  We have learned to create Views which take data from the client and dynamically return a response based on that data.  We can finally combine these two to create our JSON API.  How simple!



Let's create the CRUD views for our Planet.  They will consume and return JSON.



First we'll stub out our views.  Since Django doesn't differentiate urls by the HTTP Verb, one view will handle the *list* and *create* actions, while the other will handle the *retrieve*, *update*, and *destroy* actions.

```python
# api/views.py

def planet_list(request):
    pass

def planet_detail(request, id):
    pass

```



And our `urls.py`

```python
# api/urls.py
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^planets/([0-9]+)/$', views.planet_detail),
    url(r'^planets/$', views.planet_list),
]
```



And be sure they are registered in our main `urls.py`

```python
# swapi/urls.py

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
]
```



We now have the basic outline.  Let's fill in our List view first.  We'll want to

1.  fetch all the Planets (or a subset in this case, to keep our output readable), 
2. convert those Planet objects into dictionaries, or native python data so we can
3. convert those dictionaries into JSON which we will
4. Return as our Response.

```python
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Planet

@csrf_exempt # disable CSRF validation for this view
def planet_list(request):
    if request.method == 'GET':
        planets = Planet.objects.all()[:5].values()
        planets_dicts = [
            {
                'name': planet.name,
                'population': planet.population,
                # Etc...
            }
            for planet in planets]
        planets_json = json.dumps(planets_dicts)
        return HttpResponse(planets_json, content_type='application/json')
    else:
        data = request.POST
        # Create Planet from dictionary
        # Validate
        # save if validation is good
        # return new planet object as JSON or our errors
```



So this works!  It's very verbose (and very slow), but it demonstrates the manual process we must go through.  Let's fill in our POST for our Create view.

```python
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Planet

@csrf_exempt
def planet_list(request):
    if request.method == 'GET':
        planets = Planet.objects.all()[:5]
        planets_dicts = [
            {
                'name': planet.name,
                'population': planet.population,
                # Etc...
            }
            for planet in planets]
        planets_json = json.dumps(planets_dicts)
        return HttpResponse(planets_json, content_type='application/json')
    else:
        # convert request data from json to a dictionary and create a planet from it
        data = json.loads(request.body)
        planet = Planet(**data)
        try:
            # validate planet data
            planet.full_clean()
        except ValidationError as e:
            errors = json.dumps(e.message_dict)
            # Return validation errors as json response
            return HttpResponse(errors, content_type='application/json', status=400)
        # Save the planet and return the response as json
        planet.save()
        planet_json = json.dumps({'name': planet.name, 'population': planet.population})
        return HttpResponse(planet_json, content_type='application/json', status=201)
```



Whew!  This was very verbose and error prone.  We can run this code and use `requests` or a tool like [Insomnia](https://insomnia.rest/) to test our API endpoint.  We our the **Create** and **List** part done.  Lets fill out the **Retrieve**, **Update**, and **Delete** views.



We have our basics outline here.  We determine our action based on the HTTP verb and repeat a lot of similar steps as above.

```python
from django.shortcuts import get_list_or_404, get_list_or_404

def planet_detail(request, id):
    if request.method == 'GET':
        # retrieve object from database
        # convert to json and respond
    elif request.method == 'PUT':
        # retrieve object from database
        # convert json data to a dictionary
        # update our object
        # validate it, and save
        # respond with json object
    elif request.method == 'DELETE':
        # retrieve object from database
        # Delete it

```



```python
from django.shortcuts import get_object_or_404

@csrf_exempt
def planet_detail(request, id):
    # retrieve object from the database
    planet = get_object_or_404(Planet, pk=id)

    if request.method == 'GET':
        desired_keys = ['id', 'name', 'population']
        # create dictionary of desired keys:value pairs from our planet
        planet_data = {key: getattr(planet, key) for key in desired_keys}
        # convert to json and return that data
        planet_json = json.dumps(planet_data)
        return HttpResponse(planet_json, content_type='application/json')

    elif request.method == 'PUT':
        data = json.loads(request.body)
        # update our planet object if those keys are present in the request
        planet.name = data.get('name', planet.name)
        planet.population = data.get('population', planet.population)
        try:
            # validate planet data
            planet.full_clean()
        except ValidationError as e:
            errors = json.dumps(e.message_dict)
            # Return validation errors as json response
            return HttpResponse(errors, content_type='application/json', status=400)
        planet.save()
        desired_keys = ['id', 'name', 'population']
        planet_data = {key: getattr(planet, key) for key in desired_keys}
        planet_json = json.dumps(planet_data)
        return HttpResponse(planet_json, content_type='application/json')

    elif request.method == 'DELETE':
        planet.delete()
        return HttpResponse(status=204)
```



Go through the above code and ask yourself: **What would change if this was a different model (i.e. Starships)?  What would stay the same?**  Would you want to write this out for our 5 more times for our other models?



So what did we learn?  There's a lot of duplication.  

- We determine our action based on the request method
- We parse the JSON request to turn it into a dictionary.  Most likely this dictionary simply contains the keys we want to set on one of our objects.
- We filter or validate the data sent to us to ensure we don't set 'restricted' attributes
- we fetch the data based on a single model, generally from the `id` thats provided.
- we turn our planet objects back into a dictionary
- we then convert that dictionary to json and send it back

There are other issues as well:

- How do we handle foreign key relations?
- How do we restrict or rate_limit certain endpoints?
- How do we accept more than just JSON? i.e. XML
- Our previous approach is pretty slow.



In all fairness, this is the totally manual way.  Django provides some convenience for us in the form of [Serializer](https://docs.djangoproject.com/en/1.11/topics/serialization/)  which we can use to convert our model instances directly into JSON.  We could use the [values](https://docs.djangoproject.com/en/dev/ref/models/querysets/#values)  queryset method to get back an iterable of dictionaries, and pass that list of dictionaries to [JsonResponse](https://docs.djangoproject.com/en/1.11/ref/request-response/#jsonresponse-objects).

```python
# Getting dicts from our query rather than Planet objects.
Planet.objects.all()[:3].values()
#<QuerySet [{'id': 1, 'name': 'Tatooine', 'rotation_period': '23', 'orbital_period': '304', 'diameter': '10465', 'climate': 'arid', 'gravity': '1 standard', 'terrain': 'desert', 'surface_water': '1', 'population': '200000', 'created': datetime.datetime(2014, 12, 9, 13, 50, 49, 641000, tzinfo=<UTC>), 'edited': datetime.datetime(2014, 12, 20, 20, 58, 18, 411000, tzinfo=<UTC>)}, {'id': 2, 'name': 'Alderaan', 'rotation_period': '24', 'orbital_period': '364', 'diameter': '12500', 'climate': 'temperate', 'gravity': '1 standard', 'terrain': 'grasslands, mountains', 'surface_water': '40', 'population': '2000000000', 'created': datetime.datetime(2014, 12, 10, 11, 35, 48, 479000, tzinfo=<UTC>), 'edited': datetime.datetime(2014, 12, 20, 20, 58, 18, 420000, tzinfo=<UTC>)}, {'id': 3, 'name': 'Yavin IV', 'rotation_period': '24', 'orbital_period': '4818', 'diameter': '10200', 'climate': 'temperate, tropical', 'gravity': '1 standard', 'terrain': 'jungle, rainforests', 'surface_water': '8', 'population': '1000', 'created': datetime.datetime(2014, 12, 10, 11, 37, 19, 144000, tzinfo=<UTC>), 'edited': datetime.datetime(2014, 12, 20, 20, 58, 18, 421000, tzinfo=<UTC>)}]>
```

`

```python
# Serializing a queryset to json
from django.core import serializers
p = Planet.objects.all()[:5] # get first five planets
serializers.serialize('json', p)
# Result
'[{"model": "api.planet", "pk": 1, "fields": {"name": "Tatooine", "rotation_period": "23", "orbital_period": "304", "diameter": "10465", "climate": "arid", "gravity": "1 standard", "terrain": "desert", "surface_water": "1", "population": "200000", "created": "2014-12-09T13:50:49.641Z", "edited": "2014-12-20T20:58:18.411Z"}}, {"model": "api.planet", "pk": 2, "fields": {"name": "Alderaan", "rotation_period": "24", "orbital_period": "364", "diameter": "12500", "climate": "temperate", "gravity": "1 standard", "terrain": "grasslands, mountains", "surface_water": "40", "population": "2000000000", "created": "2014-12-10T11:35:48.479Z", "edited": "2014-12-20T20:58:18.420Z"}}, {"model": "api.planet", "pk": 3, "fields": {"name": "Yavin IV", "rotation_period": "24", "orbital_period": "4818", "diameter": "10200", "climate": "temperate, tropical", "gravity": "1standard", "terrain": "jungle, rainforests", "surface_water": "8", "population": "1000", "created": "2014-12-10T11:37:19.144Z", "edited": "2014-12-20T20:58:18.421Z"}}, {"model": "api.planet", "pk": 4, "fields": {"name": "Hoth", "rotation_period": "23", "orbital_period": "549", "diameter":"7200", "climate": "frozen", "gravity": "1.1 standard", "terrain": "tundra, ice caves, mountain ranges", "surface_water": "100", "population": "unknown", "created": "2014-12-10T11:39:13.934Z", "edited": "2014-12-20T20:58:18.423Z"}}, {"model": "api.planet", "pk": 5, "fields": {"name": "Dagobah", "rotation_period": "23", "orbital_period": "341", "diameter": "8900", "climate": "murky", "gravity": "N/A", "terrain": "swamp, jungles", "surface_water": "8", "population": "unknown", "created": "2014-12-10T11:42:22.590Z", "edited": "2014-12-20T20:58:18.425Z"}}]'
```



```python
# List View using JSONResponse
from django.http import JsonResponse
from .models import Planet

def planet_list(request):
    if request.method == 'GET':
        # We'll just use the first 10 for now to keep things readable
        planets = Planet.objects.all()[:10].values()
        planets = list(planets) # not great, but J
        return JsonResponse(data, safe=False) # need safe=False to convert a list
        # Return with a JSONResponse
```





## Enter Django Rest Framework

[django-rest-framework](http://www.django-rest-framework.org/) (or DRF) builds on top of Django to give us some very convenient tools for crafting our APIs.



First lets install it in our virtual environment:

`pip install djangorestframework`

and add it to our installed apps in `swap/settings.py`

```
INSTALLED_APPS = (
    ...
    'rest_framework',
)
```



## Serializers

[DOCS](http://www.django-rest-framework.org/api-guide/serializers/)

> Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into `JSON`, `XML` or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.



Here's an example we'll create in `api/serializers.py` of our Planet Model.

```python
class PlanetSerializer(ModelSerializer):

    class Meta:
        model = Planet
        # our subset of fields we want to make available.  Defaults to all fields.
        fields = ('id', 'name', 'population')
```

That's it!  The `ModelSerializer` looks at our model through Introspection and determines how to create itself.  Here's the output (which we can find by printing the serializer object for convenience):

```python
# in a manage.py shell
from api.serializers import PlanetSerializer

print(PlanetSerializer())
PlanetSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(max_length=100)
    population = CharField(max_length=40)
```



```python
p = Planet.objects.first()
serializer = PlanetSerializer(p)
serializer.data
print(ps.data)
# {'id': 1, 'name': 'Tatooine', 'population': '200000'}

# With multiple objects, i.e. a QuerySet
planets = Planet.objects.all()[:5] # could just as easily be the result from filter
many_serializer = PlanetSerializer(planets, many=True)
print(many_serializer.data)
#[OrderedDict([('id', 1), ('name', 'Tatooine'), ('population', '200000')]), OrderedDict([('id', 2), ('name', 'Alderaan'), ('population', '2000000000')]), OrderedDict([('id', 3), ('name', 'Yavin IV'), ('population', '1000')]), OrderedDict([('id', 4), ('name', 'Hoth'), ('population', 'unknown')]), OrderedDict([('id', 5), ('name', 'Dagobah'), ('population', 'unknown')])]

```



**Note** `serializer.data` returns dict-like objects.  Treat it as you would a normal dictionary or list of dictionaries.

As we can see, the `data` attribute returns our instance's data, using only the fields we specified.  Let's use it!  Our `List` view goes from



```python
@csrf_exempt
def planet_list(request):
    if request.method == 'GET':
        planets = Planet.objects.all()[:5]
        planets_dicts = [
            {
                'name': planet.name,
                'population': planet.population,
                # Etc...
            }
            for planet in planets]
        planets_json = json.dumps(planets_dicts)
        return HttpResponse(planets_json, content_type='application/json')
    else:
		#...
        planet.save()
        planet_json = json.dumps(
            {'name': planet.name, 'population': planet.population, 'id': planet.id})
        )
        return HttpResponse(planet_json, content_type='application/json', status=201)

```

to

```python
from .serializers import PlanetSerializer

@csrf_exempt
def planet_list(request):
    if request.method == 'GET':
        planets = Planet.objects.all()[:5]

        serializer = PlanetSerializer(planets, many=True)
        planets_json = json.dumps(serializer.data)
        return HttpResponse(planets_json, content_type='application/json')
    else:
		# ...
        planet.save()
        serializer = PlanetSerializer(planet)
        planet_json = json.dumps(serializer.data)
        return HttpResponse(planet_json, content_type='application/json', status=201)

```

A bit cleaner!  What about parsing our JSON data?  Serializers can **deserialize** data as well, by using the `data=some_dictionary` argument.



We can then get our new object back by calling the `save` method, which automatically saves the result to the database and returns our object.

```python
good_planet_data = {'name': 'Mars', 'population': '0'}
missing_planet_data = {'population': '2000'}
good = PlanetSerializer(data=good_planet_data)
good.is_valid() # True
good.validated_data # OrderedDict([('name', 'Mars'), ('population', '0')])
new_planet = good.create()
new_planet.id # 66

bad = PlanetSerializer(data=missing_planet_data)
bad.is_valid() # False
bad.validated_data # {} aka empty dict
print(bad.errors)
# {'name': ['This field is required.']}

```



Now, incorporating it into our **Create** view (since List doesn't accept any data)

**NOTE**: We'll start using `JsonResponse` for convenience rather than manually converting our dictionaries to json with `json.dumps`



```python
import json

from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Planet
from .serializers import PlanetSerializer


@csrf_exempt
def planet_list(request):
    if request.method == 'GET':
        planets = Planet.objects.all()[:5]

        serializer = PlanetSerializer(planets)
        return JsonResponse(serializer.data, safe=False)
        # safe=False because we are returning a list, not a single object
    else:
        # convert request data from json to a dictionary and create a planet from it
        data = json.loads(request.body)
        serializer = PlanetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

```



### **Challenge**

- Try and use the Serializer for the `planet_detail` view.  To pass an instance *and* some new data used to update the instance, use the following:

```python
planet = get_object_or_404(Planet, pk=id)
data = json.loads(request.body)
serializer = PlanetSerializer(planet, data=data)
serializer.is_valid() # True or False, depending on data
serializer.save() # updates original object in the database and in memory
```



- Write Serializers for the other classes (you can ignore related fields for now)
  - Feel free to leave out some fields to keep things simple.
- Write the `List` and `Retrieve` views for these other models.