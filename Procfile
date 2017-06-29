web: gunicorn --bind 0.0.0.0:$PORT run_production:app --log-file -
init: python db_create.py
upgrade: python db_upgrade.py