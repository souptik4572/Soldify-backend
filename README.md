[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Soldify Backend
### A one stop online destination for buying and selling used products

> Backend part of the application made using Flask and uses Postgres SQL for the database.
> Hosted on heroku, can be acessed from [here](https://soldify-backend.herokuapp.com) and the entire postman documentation can be found [here](https://documenter.getpostman.com/view/14121536/UV5WDxk9)

## Local Usage

### 1. Install
This uses Python3, so firstly please install python3

- Firstly we need to clone this repository and open cmd/bash at this folder

- Now we will also need some other python packages as dependencies. So it will be better if we create an exclusive virtual environment for installing these dependencies
```bash
pip install virtualenv
```
- Next we need to create a virtual environment and activate it on our current console
```bash
virtualenv env_name
```
Under mac operating system
```bash
source env_name/bin/activate
```
Under windows operating system
```bash
env_name\Scripts\activate
```
- Next we continue installing all the necessary dependencies using the requirements.txt file
```bash
pip install -r requirements.txt
```
- Finally we can start our local server by running the following command and it will accessed at http://localhost:5000
```bash
python app.py
```

## Notes
This project was created and tested under Mac but it can be used at other distros by running the above commands

Souptik Sarkar
