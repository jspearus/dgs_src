# dgs_src

Disc Golf Scorecard app With Django web framework

# command to push git commits to heroku

    git push heroku master

# command to make migrations

    (add/modify some someapp/models.py)
    2. python manage.py makemigrations 
    3. python manage.py migrate
    6. git push heroku master
    7. heroku run python manage.py migrate

    heroku run python manage.py makemigrations

# command to migrate changes

    heroku run python manage.py migrate
