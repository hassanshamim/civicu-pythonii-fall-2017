# Django Views

### - The **'C'**in **MVC**



[DOCS](https://docs.djangoproject.com/en/1.11/topics/http/views/)

Django Views are responsible for running some specific code when a client visits some specific URL.  Using GitHub as an example, the 'User' View would be responsible for finding information about a user (respos, stars, recent activity) and returning the 'user' webpage when we visit a specific URL, i.e. https://github.com/hassanshamim/.



They 'map' a URL pattern to a function to run when that URL is visited.   Here's what the whole process looks like in Django:

![Django request/response](http://rnevius.github.io/django_request_response_cycle.png)

Generally, a view does the following tasks:

- Inspects the request for specific details (i.e. query parameters, format of response (json, csv) cookies, etc ) and gathers information based on those details
- Decides how to format those details for the requester (aka the Client)
- Returns those formatted details.

**NOTE:** In traditional webapps we have a 'frontend' or actual website that the public sees and visits.  The 3rd letter in MVC (the `V`, but we call it `Template` in Django) is responsible for taking those details gathered by the View and formatting it into a HTML webpage.  Since we are focusing on APIs, we won't be dealing with Templates.



Before we start writing our view functions however, we must first associate them with a URL.  That way when we visit the URL in our browser (or via python's `requests`) we can see the results of our view function.



## Django URLs

[DOCS](https://docs.djangoproject.com/en/1.11/topics/http/urls/)

Django URLs simply associate or map a view function to a URL pattern.   Here's an example `urls.py` from the docs:

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/([0-9]{4})/$', views.year_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
```

[`url` function docs](https://docs.djangoproject.com/en/1.11/ref/urls/#url)

Here we have `urlpatterns` which is a list of URLS that django should associate with specific views.

We create our association using the `url` function provided by Django, which takes two required arguments, as well as some optional parameters.

The required arguments are:

- url regex - a regular expression which is used against the requested URL to see if it 'matches'
- the view function to be called.

Django loops over this list to find a match and calls that view function.  If nothing matches, we get a `404` error by default.



### Regular Expressions

- [REGEX practice](https://regexone.com/)
- [Helper for writing regex](https://regex101.com/)

AKA `regex`, is simply a tool to match patterns in text.  There is a lot to them, but we don't need to know everything.  Here's a quick cheatsheet:

- `^` and `$` markers match the `beginning` or `end` of the input string respectively.
- `*`, `+` will match 0 or more, and 1 or more of the preceding character or group respectively.  i.e.
  - `hello+` will match `hello`, `helloo`, `helloooo` etc but not `hell`
  - `hello*` would match all of the above, include `hell`
- `?` means the preceding character or group is optional.  i.e
  - `cupcakes?` will match `cupcake` and `cupcakes` but not `cupcakesss`
- [character groups] are surrounded by brackets and can match a list of characters inside.
  - `[bc]at` will match `bat` or `cat`
- Shorthand `\d`, `\D`, `\w`, `\s`  match a predefined group of characters.  `\d` matches any digit for example.
- {number of matches} can be specified in brackets after a group.  `a{4}` will match 4 repeating `a` characters. `\d{2}` will match any 2 digits in a row.
- `(Capture Group)` are put in parentheses.  Sometimes we want not just to check if a string *matches* a pattern, but we want to extract the data inside.  Capture groups allow us to pull whatever text is matched inside the capture group.  For example:
  - `I am (\d+) years old`  will match `I am 3 years old` and `I am 100 years old` , with the first capture group being set to `3` and `100` respectively.
- `(?P<Name>)` Named capture groups do the same as above but allow us to access the captured groups not only by position, but by name as well.

**NOTE**: Use 'raw' python strings when creating regular expressions.  They are normal strings preceeded by an `r`.  Examples:

- `r'The year is (?P<year>[0-9]{4})'`
- `r'^\d+ bottles? of beer on the wall, \d+ bottles? of beer!$'`

**NOTE2**: captured groups values are always strings.



### URLS.py

Django URLS can pass information contained *inside* the URL pattern in two ways:

- Capture groups
- Named Capture groups

Capture groups are regular groups `()` which pass the contained information to views as **positional** arguments.

Named Capture groups `(?P<year>[0-9]{4})` pass the contained information to views as **keyword** arguments.

**You cannot mix these in a single URL pattern**.  Use one or the other.

Heres the above example written using named capture groups:

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]
```



#### Namespacing URLS

[DOCS](https://docs.djangoproject.com/en/1.11/topics/http/urls/#including-other-urlconfs)

Django provides a way to add a group of urls under a namespace.  For example, if we wanted add all the views defined in our `api` app to our url configuration and ensure they all start with `/api/` we can use the `include` function django provides:

```python
from django.conf.urls import include, url

urlpatterns = [
    # ... snip ...
    url(r'^api/', include('api.urls')), # assuming our api app has a urls.py like this one
    # ... snip ...
]
```

This allows us to keep each app self contained.  We can keep all the models, views, and urls inside the app itself and have them reference and use eachother.   When we want to make it available, we simply `include` the urlconf in our main `urls.py`.  This is considered a best practice.



## Views

Views are our functions that are called when the associated URL is requested by a client.  Here's the simplest possible view:

```python
from django.http import HttpResponse # our response object we must return

def hello(request):
  return HttpResponse('Hello World')
```

**Note**: every view function takes the `request` object as its first positional argument.  This request object is how we access information about the request (URL params, request method, etc.)  Full details in the [DOCS](https://docs.djangoproject.com/en/1.11/ref/request-response/)



We can hook it up into our urls.py

```python
# in our main urls.py
from django.conf.urls import url
from django.contrib import admin
from myapp import views as myapp_views


urlpatterns = [
    url(r'^admin/', admin.site.urls), # default, set by Django
    url(r'^hello/$', myapp_views.hello), 
]
```

Now when we visit `localhost:8000/hello/` we should see 'Hello World' in the webpage.

**NEAT!**  But a little boring, as we get the same response back every time we call it.  Let's make it dynamic by having our `hello` function greet the name if we provide it.   One way to do this is with a query string.  So visiting `localhost:8000/hello/?name=Winnie` we should get back a `Hello Winnie` response.



```python
from django.http import HttpResponse # our response object we must return

def hello(request):
    if 'name' in request.GET: # a dictionary of our querystring parameters
        name = request.GET['name']
    else:
        name = 'World'
    text = "Hello %s" % name
    return HttpResponse(text)

```

Since we are just looking for an optional query string, we don't need to change our urlpattern at all.

If we want to 'store' that `name` in the url, we can use a capture group in our url pattern, and pass it into the view function as an argument.  Now the `name` is a requirement of the URL.

```python
# in our main urls.py
from django.conf.urls import url
from django.contrib import admin
from myapp import views as myapp_views


urlpatterns = [
    url(r'^admin/', admin.site.urls), # default, set by Django
    url(r'^hello/([A-Za-z]+)/$', myapp_views.hello), 
]
```

```python
# my_app/views.py
from django.http import HttpResponse # our response object we must return

def hello(request, name):
    text = "Hello %s" % name
    return HttpResponse(text)

```



If we want to allow a default `name` to fall back on, we can used named capture group to pass the `name` value as a keyword argument.  Unfortunately our URL needs the capture group or it will fail.  If we leave the capture group empty, with `localhost:800/name//`, then an empty string will be matched.



A common pattern to provide defaults is to have another URL without the capture group point to the same view.  Since we provide a default value in our view, that will be used.

```python
# in our main urls.py
from django.conf.urls import url
from django.contrib import admin
from myapp import views as myapp_views


urlpatterns = [
    url(r'^admin/', admin.site.urls), # default, set by Django
    url(r'^hello/$', myapp_views.hello), 
    url(r'^hello/(?P<name>[A-Za-z]+)/$', myapp_views.hello), 
]
```

```python
# my_app/views.py
from django.http import HttpResponse # our response object we must return

def hello(request, name='World'):
    text = "Hello %s" % name
    return HttpResponse(text)
```





## Practicing Views

**Note**: You will need to register the below views in your `urls.py` to view them in the browser.

- Create a view 'hello' which just displays 'hello world'

- create a view 'current_time' which displays the current time

  ```python
  from datetime import datetime
  datetime.now()
  ```

  ​

- Create view 'counter' which displays a number, starting at 1.  Each time this URL is visited the counter increments by one.  So firts visit will be '1', second will be '2', etc.

  - Now edit this view so it accepts a query parameter `increment`.  The value will be an integer which increases the counter by that much.  So if visiting /counter/ displays `5`, visiting `/counter/?increment=0` will display `5` again.  then visiting `/counter/?increment=4` will display `9`
  - **HINT**: you cannot modify variables in the global scope without the `global` statement.

- Create a 'calendar' view.  It takes one parameter - the year. Use the following snippet to get a string representation of the calendar to return to the user.  **Note** It won't be very pretty.

- ```python
  from calendar import HTMLCalendar
  cal_obj = HTMLCalendar()
  result = cal_obj.formatyearpage(year) # result is a string
  ```

  ​

- Create a view for looking up one of your models its primary key.  Display its name or title.

- Convert one of your previous views to return a `json` response.  You can use the `JsonResponse` object provided by django as follows:

  ```python
  from django.http import JsonResponse

  def example_view(request):
    data = {'a': 1, 'b': 2}
    return JsonResponse(data)
  ```



## Bonus Challenge

- Add a `likes` integer field to the Film model.  Create a migration and apply it.  Then create a view which allows you to increase the 'likes' of a chosen Film by 1.  Add another view which displays the number of likes a Film has.  Note: use whatever value you'd like to lookup the Film  Using it's primary key is traditional