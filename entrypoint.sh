python manage.py migrate
python manage.py loaddata fixtures/user.json
python manage.py loaddata fixtures/res_cat.json
python manage.py loaddata fixtures/res.json
python manage.py loaddata fixtures/food.json
gunicorn pubsub.wsgi:application --bind 0.0.0.0:8000
