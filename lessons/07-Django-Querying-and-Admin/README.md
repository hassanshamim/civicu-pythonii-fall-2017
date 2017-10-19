# Review



### Today's objectives

1. Review Process of Defining a new model and creating/running migrations
2. Understand how to query and create Model objects through the `model.objects` manager
3. Customize the admin interface of these models to suit our needs



## Review

### Models

[DOCS](https://docs.djangoproject.com/en/1.11/topics/db/models/)

Django web applications access and manage data through Python objects referred to as models. Models define the *structure* of stored data, including the field *types*.

By defining a new model, you instruct the database *how* to store the data associated with that object, as well as the properties said object will have when retrieved from the database.  For example:



```python
# models.py
from django.db import models

class Student(models.Model):
  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
  
    def full_name(self):
        return self.first_name + " " + self.last_name
```



Will tell Django to create a table called `Student` in the database.  The table will have the following fields (or columns):

- `id` which is an integer and is automatically added when a new row is saved to the database


- `first_name` which stores a string


- `last_name` which stores a string
- `birthday` which stores a date.

**NOTE**: since `full_name` is a method and not a Field, the database will not create a column for it.

When we query the database for a student, for example with one named 'Michael Shannon', we get an *instance* of the Student class - aka a *Student object*.  The Student object has all the declared fields as attributes.

Creating a Student and saving it to the database

```python
import datetime
from .models import Student

# Initializes the Student object.
jim = Student(first_name='Jim', last_name='Miller', birthday=datetime.date(1990, 8, 23))
# we can access its associated fields as attributes
jim.first_name # 'Jim'
# Since it is a python object and we defined a method 'full_name' inside its class, it may access that method
jim.full_name() # 'Jim Miller'
# Saves the student object as a new row in the Student table
jim.save() # the `id` attribute is automatically set the first time a new object is saved
jim.id # 1  

# Retrieve the Student from the database with id of 1
result = Student.objects.get(id=1)
result.full_name() # 'Jim Miller'
```



#### Model Meta

[DOCS](https://docs.djangoproject.com/en/1.11/ref/models/options/)

Models may have an optional `class Meta` inside them, which defines some optional information about the Model.  For example:

```python
from django.db import models

class Student(models.Model):
  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    
    class Meta:
          ordering = ['birthday'] # Specifies default ordering when returning a query
  
    def full_name(self):
        return self.first_name + " " + self.last_name
```

Will result in all queries of the `Student` model ordered by the students birthday (ascending by default).



#### Migrations

[DOCS](https://docs.djangoproject.com/en/1.11/topics/migrations/)

In order to keep your database in sync with your Models, Django provides a `migrations` utility.  Migrations are automatically generated from your models (when the command `makemigrations` is given), and instruct the database on any *changes* it needs to make to the database schema in order to hold all the data as described in your models.  Think of it as version control for the *structure* of your database.  Migrations can also be used to transform the **data** inside your database.



The general workflow when working on a new model or editing a previous model is:

- Edit the `Model` class in your `/app_name/models.py` file
- Have django generate the migrations (instruction set) for you: `python manage.py makemigrations`
  - This creates a new migrations file in the `migrations` folder of your specified app.
- Apply those migrations to change your database: `python manage.py migrate`



#### Relationships

[DOCS](https://docs.djangoproject.com/en/1.11/topics/db/models/#relationships)

Very rarely will all your Models be self contained.  More often, they have a relationship with one or more other models.  For example, if we were creating an app that catalogued music, we might have the following:

```python
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

Here, we have two models: `Musician` and `Album`.  A musician may *have many* albums, or said differently - an album *belongs to* a musician.  This is known as a **One to Many** relationship and we use a `ForeignKey` field to allow our `Album` model to reference a `Musician`.  You can traverse these relationships when querying or from the objects themselves.

**Note:** the `on_delete=models.CASCADE` parameter instructs an Albums on how to react if their related object is deleted.  In this example, if we delete a Musician from our database, all their associated Albums will be deleted as well.

The two you will use most often are:

- ForeignKey
- ManyToManyField



## Practice Challenge

Create a new django app (in a fresh django project or in an existing one) named `library` and add some new models to `library/models.py` with the specifications below.  When you are done, run your migrations and register these models in the Admin Interface.

**Note: be sure to add your new app to the INSTALLED_APPS list in settings.py**

Test your models manually by adding a few via the Admin Interface or the `manage.py shell`.

**Genre**

- String Fields:
  - name
- Relationships:
  - has multiple books

**Author**

- String Fields:
  - name
- DateField
  - Date of Birth
  - Date of Death (can be NULL)
- Relationships:
  - has multiple books

**Book**

- String fields:
  - title
  - summary
  - ISBN
- number fields:
  - pages
- Relationships:
  - has an Author (can only have one)
  - has multiple Genres





## Querying

### [DOCS](https://docs.djangoproject.com/en/1.11/topics/db/queries/)

**Note:** Sometimes its useful to see the actual queries that hit the database.  The easiest way to view this is is to use the `django-extensions` package.  Simply `pip install django-extensions` , add `django_extensions` to your `INSTALLED_APPS`, and then enter the django shell with:

`python manage.py shell_plus --print-sql`

`shell_plus` will automatically import all your Models for you.

------

There's no way I can cover all the details of querying your models.  Instead, I offer a quick reference and some notes.

Using our `Book` example from above:

#### Get a book with id 15.  Fails if 0 or more than one object is returned

`Book.objects.get(id=15)`

#### Get all books with the word 'the' in the title.

`Book.objects.filter(title__contains='the')`

#### Get all books with an author whose name contains 'Bob'

`Book.objects.filter(author__name__contains='Bob')` **Note: can be case insensitive with `__icontains`**

#### Get all books with a specific Author

`Book.objects.filter(author__id=15)`

or, if we already have the desired Author as an object assigned to the variable `some_author`:

`some_author.book_set.all()`  Here, the 'related_name' is  not set so it gets defaulted to the property name + `_set`

#### Get all books with less than 300 pages

`Book.objects.filter(pages__lte=300)`



## Validate before Saving Objects

[DOCS](https://docs.djangoproject.com/en/1.11/ref/models/instances/#validating-objects)

When creating new objects, be careful when saving them.  For example:

```python
got = Book(pages=900)
got.save() # Raises an error because it doesn't have an Author
got.author_id = 1 # just set it to the first author in the database
got.save() # No errors!  Wait a minute... it doesn't have the required title!
```

`Model.save()` doesn't do any proper validation of required fields.  The only reason it complained about the `author_id` in the above example is because the Database requires it.  To validate your object before saving it, you should call `full_clean` on the object:

```python
got = Book(pages=900)
got.full_clean() 
# ValidationError: {'title': ['This field cannot be blank.'], 'summary': ['This field cannot be blank.'], 'isbn': ['This field cannot be blank.'], 'author': ['This field cannot be null.']}
got.title = 'Game of Thrones'
got.full_clean()
# ValidationError: {'summary': ['This field cannot be blank.'], 'isbn': ['This field cannot be blank.'], 'author': ['This field cannot be null.']}

```



### Race Conditions

Sometimes you'll want to update an object based on its existing state.  For example, if we had a `num_sales` on our `Books` class that we want to increment, we might write our query like so:

```python
book = Book.objects.get(id=42) # query
book.num_sales = book.num_sales + 1 # update object
book.save() # reflect our changes in the database
```

Unfortunately, there is a delay between our query in line 1 and sending the data to the database in line 3.  In that time another query may update that same book!  Now our `num_sales` will be incorrect.



The solution to this problem lies in Django's [F expressions](https://docs.djangoproject.com/en/1.11/ref/models/expressions/#django.db.models.F).  This is some magic that retrieves a value based on the existing value of that row in the database.  F expressions are also useful for complex queries, you can read the documentation for more info.  The correct way of doing the above is below:

```python
from django.db.models import F

book = Book.objects.get(id=42)
book.update(num_sales=F('num_sales') + 1)

# or in one line
Book.objects.get(id=42).update(num_sales=F('num_sales') + 1)
```





## Admin Interface

[DOCS](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/)

The Django Admin interface is a powerful tool.  It lets us avoid writing basic forms to view and manipulate our data (on our end - don't expose it to customers!) which gives us the added benefit of letting non-technical users manage the data of the application.



Unfortunately, the default is very bland.  It lets us view and edit individual objects, but thats not very impressive.  Fortunately, we can extend it in many ways.  We'll stick to simple configuration options exposed to us via Django, but you can absolutely add custom themes and widgets if you'd like.



First, we'll practice on our Planet models since it is simple.  Right now, our `api/admin.py` looks something like this:

```python
from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.Planet)
admin.site.register(models.People)
admin.site.register(models.Species)
admin.site.register(models.Vehicle)
admin.site.register(models.Transport)
admin.site.register(models.Starship)
admin.site.register(models.Film)

```



To customize our Admin interface, first we need to create a `ModelAdmin` class:

```python
from django.contrib import admin
from api import models

class PlanetAdmin(admin.ModelAdmin):
    pass


# Register the model with the admin
admin.site.register(models.Planet, PlanetAdmin)
```

So far the end result is the same.  We just manually associated the Admin with the Model.  Django does this under the hood for us in the previous version.

To customize our `PlanetAdmin`, edit the following lines and refresh your admin page:

```python
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'population', 'surface_water'] 
```

Now our Planet Admin page displays not *just* the name, but also the population and surface_water as well.  



We can display not just existing fields, but the results of our model methods or functions themselves.  For example:

```python
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'population', 'gravity', 'has_enough_water']
    def has_enough_water(self, obj):

        water = obj.surface_water
        if not water.isdigit():
            return False
        return int(water) > 10
    has_enough_water.short_description = 'Habitable?'

```

Will add a new column titled 'Habitable?' with either True or False.



We can optionally filter our models based on a field as well:

```python
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'population', 'gravity', 'has_enough_water']
    list_filter = ['gravity']
    def has_enough_water(self, obj):

        water = obj.surface_water
        if not water.isdigit():
            return False
        return int(water) > 10
    has_enough_water.short_description = 'Habitable?'
```

Though generally this option works best on fields with a `choices` parameter set.



The `fields` option allows us to control how our Planet Form appears, and what fields are present.   For example, if we only want to allow editing of the 'name' and 'population' fields on the model, we can add the following:

```python
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'population', 'gravity', 'has_enough_water']
    list_filter = ['gravity']
    fields = ['name', 'population']
```

This is very useful if you have certain fields set indirectly (i.e. Account Balance for a bank).



Lastly, Django allows us to write custom actions that operate on a set of objects.  For example, to generate a JSON dump of the selected objects, we could add the following:

```python
from django.http import HttpResponse
from django.core import serializers

class PlanetAdmin(admin.ModelAdmin):
    actions = ['export_as_json']
    
	def export_as_json(self, request, queryset):
   		response = HttpResponse(content_type="application/json")
    	serializers.serialize("json", queryset, stream=response)
    	return response
```

Normally, you will use this to change some state of selected objects:  i.e. 'Cancel Orders', 'Publish Article', etc.



**Challenges:** 

- Play around with the admin interface, read the docs, and change anything you don't like.
- Add an Admin action to export selected planets as a CSV file.  (Hint: you'll need to use your Google-Fu)
- Go through parts 1-2 of the official [Django Intro](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)