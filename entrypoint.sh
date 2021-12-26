echo "Waiting for server to RUN ... "
cd listingproject
python3 manage.py migrate --noinput
python3 manage.py test reservation 
python3 manage.py  runserver 0.0.0.0:8000