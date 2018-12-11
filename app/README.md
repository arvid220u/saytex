# saytex api

Install by running

`./setup.sh`

Copy config and add API keys:

```cp config_template.py config.py
vim config.py```

Activate the virtualenv:

`source venv/bin/activate`

Run in production:

`./run-production.sh`

Kill it:

`killall gunicorn`
