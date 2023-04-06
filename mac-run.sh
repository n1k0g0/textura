#!/bin/bash

source textura_env/bin/activate

python textura_site/manage.py migrate 

python textura_site/manage.py runserver
