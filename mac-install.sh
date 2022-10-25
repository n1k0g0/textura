#!/bin/bash
python3 -m pip install --user --upgrade pip

python3 -m pip install --user virtualenv

python3 -m venv textura_env

source textura_env/bin/activate

python3 -m pip install --user --upgrade pip

python3 -m pip install Django 

python3 -m pip install -r requirements.txt

deactivate