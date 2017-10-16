## Class Lesson Plan

- Review last exercism (hamming)
- Clone [example django repo](https://github.com/hassanshamim/swapi-models), install django
- Overview of Django MVC
- Introduction to writing Models
- Managing the database - migrations
- Querying the database
- Writing tests?



Useful Django links:

- [Official Django Docs - Models](https://docs.djangoproject.com/en/1.11/topics/db/models/)
- [Offical Django Docs - Querying](https://docs.djangoproject.com/en/1.11/topics/db/queries/)
- [DjangoGirls Beginner Tutorial](https://tutorial.djangogirls.org/en/)
- [Official Django Tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)



Commands I ran when setting up today's demo repo:

- `django_admin startproject swapi` to generate initial skeleton
- `python3 -m venv env` to create virtualenv
- `source env/bin/activate` to activate virtual env
- `pip install django`
- `pip freeze > requirements.txt`
- `manage.py startapp api` to generate the `/api/` folder or 'app'
- Edited `settings.py` to include `api` in INSTALLED APPS
- Imported and registered some models in `api/admin.py`



Your Directions:

- clone repo, create virtual env (in main swapi folder next to manage.py), activate

- `pip install -r requirements.txt`

- Setup Database:
  `manage.py migrate`
  `manage.py loaddata transport.json `
  `manage.py loaddata vehicles.json`
  `manage.py loaddata starships.json`

- `manage.py createsuperuser` and fill out with something easy to remember (you can reset it)

- Look at example model in`api/models.py`

- Fill in missing class definitions:

  - Find associated json file

  - try to load it:

  - `manage.py loaddata planets.json`

  - `KeyError: 'population'` : fill in the missing field (hint: it's probably a CharField)

  - `django.db.utils.OperationalError: Problem installing fixture '...swapi/api/fixtures/planets.json': Could not load api.Planet(pk=1): no such table: api_planet` Means the only thing not working is the lack of a table in your database!

  - Create the table in your database now:

    - `manage.py makemigrations `
    - `manage.py migrate`

  - Load the data again: `manage.py loaddata planets.json`

  - `./manage.py loaddata planets.json`

    - `Installed 60 object(s) from 1 fixture(s)`
    - It worked!

  - To view your loaded data, do either (or both) of the following:

    - in `api/admin.py` add the model as follows (using Planet as an example):

      - `admin.site.register(models.Planet)` 
        run your server `manage.py runserver`
        visit admin `http://127.0.0.1:8000/admin/api/`
        Visit your model page
        View one of the rows in your database.  Feel free to edit it or add a new one.

      - in a django shell: `manage.py shell`

      - ```python
        from api import models
        models.Planets.objects.count() # shouldn't be 0
        ```

        ​





Challenges:

- Give each model a `__str__` method that returns the model's name or title.  How does this additional affect the django admin results or your ORM results?


- Some of these fields are stored as strings when numbers would be better.   Try converting the `cost_in_credits` field in `Transport` to store a number instead of a string.  Hint: You need a different field than `CharField`.
- There is quite some duplication  Each of our models has a `created` and `edited` field.  We can extract these attributes into an [Abstract base model class](https://docs.djangoproject.com/en/1.11/topics/db/models/#abstract-base-classes), and then inherit from that model for each of our models we use.  Create an Abstract Base Model named `TimestampedModel` with the two fields listed above, and change our listed models to use said field.  (ignore `Transport` and `Vehicle` models.)



Querying:

- How many Starships are there?
- How many Films did George Lucas direct?
- What is the *latest* film George directed?
- What is the name of the Starship with `id` 15?
- How many films was that starship in?
- How many films was the starship with the name 'CR90 corvette' in?
- Which Film had the fewest Starships?
- Which Films did Luke Skywalker (id=1) did *NOT* appear in?
- How many Starships have a name with the word `fight` in it? (Case insensitive)
- What is the cheapest starship? (cost in credits)