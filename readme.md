# Listing Project
## To run the project use :
``` 
docker-compose -f docker-compose.yml run -d
```

## To run tests use (If you do not want to use docker compose) :
```
python3 manage.py test reservation 
```

## URLs : 
```
pages
-----
Home         [GET]  : http://127.0.0.1:8000/reservation/
Owner Home   [GET]  : http://127.0.0.1:8000/reservation/<int:owner_id>/
House Page   [GET]  : http://127.0.0.1:8000/reservation/<int:owner_id>/house/<int:house_id>/
Create House [POST] : http://127.0.0.1:8000/reservation/<int:owner_id>/house/
Update House [POST] : http://127.0.0.1:8000/reservation/<int:owner_id>/house/<int:house_id>/

API endpoints
-------------
API Roots    [GET]  : http://127.0.0.1:8000/reservation/api-v1/
Reserve Room [POST] : http://127.0.0.1:8000/reservation/api-v1/rooms/reservation/

```

## NOTE: Sqlite database included
## Admin user 
```
username : bijan
password : 1
```
