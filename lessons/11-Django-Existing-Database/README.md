# Building an API from Existing Database

### [Description of the Chinook Database](http://www.sqlitetutorial.net/sqlite-sample-database/)



repo url for reference: https://github.com/hassanshamim/chinook_practice/

it has the following branches:

- **model-edits** - contains all the neccesary (although crude) changes to that you can start building your API
- **basic-api** - ***(solution)*** contains a simple implementation of the api which you will work on in class today.

##### useful links:

http://www.cdrf.co/3.7/ - A nice reference for DRF class based views

https://docs.djangoproject.com/en/1.11/topics/db/multi-db/ - How to handle multiple databases

[Using Django Database Routers](https://docs.djangoproject.com/en/1.11/topics/db/multi-db/#using-routers)



#### The process:

- download sqllite database
- create virtualenv
- create chinook project (django-admin start project)
- create a new app (I will call it `api` for simplicity)
- Generate models.py `python manage.py inspectdb > api/models.py`
- Fix models (as described in your new models.py)
- create serializers
- create API views
- configure urls.py
- Visit browser and test manually