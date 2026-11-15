# Brevet Time Calculator with MongoDB database 

This project is a reimplementation of the RUSA ACP controle time calculator using Flask and AJAX. It also stores the calculated times in a MongoDB database

## Dependancies
This project uses the python libraries:
* arrow
* Flask
* nose
* pep8
* autopep8
* python 

Which can be installed using Python-Pip

This project also relies on the Docker MongoDB image, although you can use the frontend attached to any instance of MongoDB

## Usage
### Starting the Server
* Make a copy of the "credentials-skel.ini" file, named credentials.ini and fill out all the details.
* Run "docker compose up --build" in your terminal

### Using the Program
* Set the time, date and brevet at the top of the page.
* Type the distances of your controls. As you do the times should begin to appear
* Clicking "submit" will save all the times you've typed in into the database
* Clicking "display" will show any saved times from the database

## Testing
This project uses Python Nosetests. Install python-nose and then run "nosetest" in the root of the brevets directory.
 The server needs to be running for test_webapi.py to be working.
## Credits

acp_times and other bits and bobs written by Enzo Neuschwanger (eneuschw@uoregon.edu)

Everything else is from UO CS322

