# Installation guide

Just build and run docker containers
```
docker-compose up --build -d
```

Then log into webapp container and create django superuser

```
python manage.py createsuperuser
```

Database is seeded with initial data
Api is hosted on http on 0.0.0.0:80