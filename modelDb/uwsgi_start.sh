#!/bin/bash
uwsgi --http 0.0.0.0:80 --file modelDb/wsgi.py --static-map=/static=static

