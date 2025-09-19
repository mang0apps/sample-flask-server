# INSTRUCTIONS

## To run on Windows

1) Install first, `pip install waitress`
2) `waitress-serve --host 0.0.0.0 --port 5000 app:app`

## TO run on Linux

1) Install first, `pip install gunicorn`
2) `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
