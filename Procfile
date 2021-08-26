
.listen(process.env.PORT || 5000)
web: gunicorn --pythonpath bot_for_heroku bot_for_heroku.wsgi --preload -b 0.0.0.0:$PORT
worker: python bot_for_heroku/manage.py collectstatic --noinput
web: python bot_for_heroku/manage.py runserver 0.0.0.0:5000 --noreload
