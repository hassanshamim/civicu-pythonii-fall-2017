# DRF API Views

This Lesson's Code can be found in the 'drf-api-2' branch of the `swapi-models` repo. [LINK](https://github.com/hassanshamim/swapi-models/tree/drf-api-2/)

### Objectives

- Learn how and when to use Class Based Views
- Become familiar with `rest_framework` Request/Response objects
- Enable the Browsable API
- Introduce Generic Views
- (maybe) Add Custom Serializer that handle foreign key relations





## DRF Request/Response Objects

DRF comes with it's own `Request` and `Response `objects that we use in the same way as the `request` object we pass into our views and our `HttpResponse` or `JsonResponse` that we return.  When using DRF's views instead of Djangos, these will be used automatically.



#### The Benefits

**DRF** **Request**

[DOCS](http://www.django-rest-framework.org/api-guide/requests/)

`request.data` gives us the data sent along with the request, already parsed into default python data types.  This saves us from using the `json` module to parse the `request.body` as we do in our vanilla Django Views.  We can use it for any request type with data attached: 'PUT', 'POST', and 'PATCH' are all fine.  It also allows us to consume multiple formats, i.e. `xml`, `json`, and `form` data are all fine, as long as we configure our application to allow them.

`request.query_params`

Is how we get query parameters in the URL of the request.  This is just like `request.GET` in Django.

**DRF Response**

[DOCS](http://www.django-rest-framework.org/api-guide/responses/)

Automatically renders the response in the correct format as requested by the client.  Just like the `Request` object, this can be `xml`, `json`, `html`, etc.  We can use it like so:

```python
@api_view
def some_view(request):
  # get the object, put it in a serializer
  return Response(data=serializer.data)
```



return Response(data=serializer.data)`

No need to explicitely convert to abritrary data formats.  This is handled for you.



#### Status Codes

[DOCS](http://www.django-rest-framework.org/api-guide/status-codes/)

DRF comes with a `status` module from which we can use well named variables to represent the status codes we want.  This is preferred to using an integer as it is more explicit.

example:

```python
from rest_framework import status
from rest_framework.decorators import api_view

@api_view
def some_view(request):
    return Response({'hi': 'there'}, status=status.HTTP_200_OK)
    
```





## Using the @api_view decorator

[DOCS](http://www.django-rest-framework.org/api-guide/views/#function-based-views)

DRF provides a wrapper function, `api_view` to convert our function based views into DRF function views.

This allows us to use their `Request` and `Response` objects nicely, as well as allowing us to configure the other niceties DRF provides (pagination, throttling, content-negotiation, etc).



Here's what a `people_list` view for our `People` Model would look like:

Notice we just use `request.data` and return a `Response`.  We don't worry about JSON at all.

```python
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import People
from .serializers import PeopleSerializer

@api_view(['GET', 'POST']) # Automatically return HTTP 405 if the request type is not set
def people_list(request):
    if request.method == 'GET':
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)
    else:
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```



As practice and review, take a moment to implement the `peoples_detail`  using the `@api_view` decorator.  For convenience, the serializers, urls, and the beginning is provided:



```python
# in api/urls.py
urlpatterns = [
    #...
    url(r'^people/$', views.people_list, name='people-list'),
    url(r'^people/(?P<pk>[0-9]+)/$', views.people_detail, name='people-detail'),
]
```



```python
# in api/serializers.py
from rest_framework import serializers

from .models import Planet, People

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('id', 'name', 'birth_year', 'homeworld')

```



```python
# in api/views.py

@api_view(['GET', 'PUT', 'DELETE'])
def people_detail(request, pk):
    person = get_object_or_404(People, pk=pk)

    if request.method == 'GET':
        # ... and so on
```



```
# Some test commands for you to use:

## Get detail for yoda
curl --request GET \
  --url http://localhost:8000/api/people/20/
  
## Create a new person
curl --request POST \
  --url http://localhost:8000/api/people/ \
  --header 'content-type: application/json' \
  --data '{
		"name": "Zam Wesell",
		"birth_year": "unknown",
		"homeworld": "3"
}'

## Update a person
curl --request PUT \
  --url http://localhost:8000/api/people/60/ \
  --header 'content-type: application/json' \
  --data '{
	"name": "Gregar Typho",
	"birth_year": "who knows",
	"homeworld": 8
}'

## Delete person 60
curl --request DELETE \
  --url http://localhost:8000/api/people/60/
```





## Browsable API

Let's add the ability to browse our api from the webpage.



To do this, simply:

- add a `format=None` keyword argument to our views
- use the `format_suffix_patterns` provided by DRF.

In our `api/urls.py`

```python
from django.conf.urls import url
from . import views

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^planets/$', views.planet_list, name='planet-list'),
    url(r'^planets/(?P<pk>[0-9]+)/$', views.planet_detail, name='planet-detail'),
    url(r'^people/$', views.people_list, name='people-list'),
    url(r'^people/(?P<pk>[0-9]+)/$', views.people_detail, name='people-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

```

in our `api/views.py`

```python
def people_list(request, format=None):
    #... body of function stays the same

def people_detail(request, pk, format=None):
    # rest stays the same
```



Now if we `python manage.py runserver` and visit our people endpoint at http://localhost:8000/api/people/ we should see a webpage if our response, and an editor to send data to the endpoint.



## Class Based Views

[DOCS](http://www.django-rest-framework.org/api-guide/views/)

Looking good so far!  But still lots of repetitive logic between our views.  Let's see briefly what the `People` view would have looked like as a Class Based View.  This is a single object that has multiple methods that map to our request methods (GET, PUT, DELETE, etc.)

```python
# api/views.py
class PeopleList(APIView):

    def get(self, request, format=None):
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleDetail(APIView):

    def get_object(self, pk):
        try:
            return People.objects.get(pk=pk)
        except People.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PeopleSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializers = PeopleSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

And using it in our `urls.py` is a little different.  All we do is call `as_view` on the object.

```python
# api/urls.py
urlpatterns = [
    #...
    url(r'^people/$', views.PeopleList.as_view(), name='people-list'),
    url(r'^people/(?P<pk>[0-9]+)/$', views.PeopleDetail.as_view(), name='people-detail'),
]
```



So it looks almost exactly the same.  What's the point?

- get_object is a good example.  It allows us to reuse code particular to that view
- data is attached the the View object.  for example, we can assign permissions, authentication, throttling etc. by just declaring it on our view class



For example, here's a simple view which only accept token authentication and will only work if the user has admin priveledges. 

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```



## Generic Views

[DOCS](http://www.django-rest-framework.org/api-guide/generic-views/)

`from rest_framework import generics`

Since there is so much repetition, DRF provides some `generics` that implement the `list`, `create`, `retrieve` `update` and `delete` operations for us.  All we need to do is tell the view what serializer and queryset to use.  We can also specify the permission, authenticationn, and pagination like above.

We can use them all bundled together, or create our own via [mixins](http://www.django-rest-framework.org/api-guide/generic-views/#mixins), which just implement one of the above.

Let's see what our `species` endpoints would look like if we used the generics.

```python
# api/views.py
# species generic views
from rest_framework import generics
from .serializers import SpeciesSerializer
from .models import Species

class SpeciesList(generics.ListCreateAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class SpeciesDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

```



The `SpeciesList`, for example, is equivalent to:

```python
from rest_framework import mixins
class SpeciesList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
```

Where we explicitely state which CRUD commands we want to include.  



To use a generic view in your urls, use it just like the previous `ApiView` 

```python
# api/urls.py
urlpatterns = [
    #...
    url(r'^species/$', views.SpeciesList.as_view(), name='species-list'),
    url(r'^species/(?P<pk>[0-9]+)/$', views.SpeciesDetail.as_view(), name='species-detail'),
]
```



And that's it!  We could even reduce repetition a little further by using [ViewSets](http://www.django-rest-framework.org/api-guide/viewsets/), which allow us to bundle our `List` and `Detail` views into one, as well as let us automatically generate urls.  I invite you to explore this functionality on your own if you'd like.





## Extending your API

You can include all sorts of extra functionality that we haven't covered here.  For a few ideas, check out the [API Guide](http://www.django-rest-framework.org/#api-guide) from the DRF docs.  Generally the process will be either changing the setting in `settings.py` or inheriting from a class provided by DRF and changing some defaults.  Let's take pagination as an example.



#### Pagination

To set default pagination, simply tell DRF how you want your responses paginated.  This is done system-wide in  `settings.py`



```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

```

Now all your API views will by default paginate with 10 items max.  If we want to allow up to 50 results on a specific endpoind, we create our own class and bind it to that view.



```python
from rest_framework import pagination

class LargeResultsPagination(pagination.PageNumberPagination):
    page_size = 50  # default number returned in a page
    max_page_size = 50  # maximum allowed

class SpeciesList(generics.ListCreateAPIView):

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    pagination_class = LargeResultsPagination
```



## Challenge

- Create Generic views for the rest of the models
- Give `ViewSets` a whirl.  Do you prefer them?
- Switch from `ModelSerializer` to `HyperlinkedModelSerializer` Does this break things?  What's a sensible solution?
  - No 'correct' answer here.  All opinions are welcome
  - the official swapi API doesn't accept POST/PUT arguments, so thats how they work around the issue.
- Add some other customizations, i.e. pagination, throttling, authorization