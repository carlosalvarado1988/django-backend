# Django Backend

## Setup the local env

create a virtual environment

> python3.11 -m venv venv
> source venv/bin/activate

add file requirements.txt with the following info:

> django>=4.00,<4.1.0
> djangorestframework
> pyyaml
> requests
> django-cors-headers

then run the following commands to install the dependencies

> pip install -r requirements.txt
> pip install --upgrade pip

create two folders: backend and client.
navigate to backend folder and run the following command to install the framework

> django admin startproject cfehome .

## Run the local env

run the server

> source venv/bin/activate
> cd backend/
> python3 manage.py runserver 8000

run a client file:

> python3 client/details.py

course video: https://www.youtube.com/watch?v=c708Nf0cHrs
course time: 2:04min
