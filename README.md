# insurance_api

### System requirements:

* Unix
* Python3.8
* PostgreSQL

### To initialize application:
```
cp dotenv.example .env
python3.8 -m venv anenv
source anenv/bin/activate
sh setup.sh
```

### To run the application
```
flask run
```
(CTRL+C to quit)

### To run tests
```
python -m pytest tests/
```

### More information:

* After initializing the app it would be a good idea to change SECRET_KEY and JWT_SECRET_KEY in your .env file to something a bit more secretive.
* Feel free to set your psql db to whatever uri you would like, just make sure to update .env and setup.sh before (re)running setup.sh.


### Examples of successful requests can be run in Postman here

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/654145739aa4e365a1c0)
