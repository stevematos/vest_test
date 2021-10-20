# VEST TEST

Requirements:
 - Python 3.6.9 >
 
Steps to install it:

1. Clone the repository:

```.shell script
    git clone https://github.com/stevematos/api_rss_reader
```
  
2. Create and activate the virtual environment:
```.shell script
    virtualenv env -p python3
    source env/bin/activate
```
   

3. Install requirements:
```.shell script
    pip install -r requirements.txt
```

4. Run the application, if you want to run it in dev mode add --reload:
```.shell script
    uvicorn main:app [--reload]
```
You can also run runserver.sh to deploy the application.

The application will be running at http://127.0.0.1:8000

If it is the first to be run by the application, the database will be created automatically
 in sqllite called database.db.

If you want to run the unit tests you do it with the command
```shell script
    python -m unittest tests/endpoints.py  
```
PSDT: A database called test.db will be created that is created when you start the tests and the tables will be dropped when the tests are finished.
## PROJECT STRUCTURE

```
VEST_TEST
│   readme.md 
│   main.py
│   .gitignore
│   requirements.txt
│
└───api : package for using APIs
│   
└───crud: package use of the different interactions with the database
│   
└───db: contains everything related to database connections
│   
└───models: contains the database models used in the applications 
│   
└───schemas: schemes used in the application
│   
└───test: contains the application tests
│   
└───utils: functions that are reused in the application
```

Developed by: [Steve Matos](https://github.com/stevematos)