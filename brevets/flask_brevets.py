"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import pymongo # Database
import os      # For getting enviroment variables

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = pymongo.MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.brevetdb
collection = db.brevetdb
collection.drop()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    race_distance = request.args.get('race_distance', 999, type=float)
    #time_zone = request.args.get('utc_offset')
    date = arrow.get(request.args.get('day') + ' ' + request.args.get('time'), 'YYYY-MM-DD HH:mm', tzinfo='utc')
    print(date)
    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet={}".format(race_distance))
    app.logger.debug("request.args: {}".format(request.args))
    app.logger.debug("date: {}".format(date))
    open_time = acp_times.open_time(km, race_distance, date)
    close_time = acp_times.close_time(km, race_distance, date)
    result = {"open": open_time, "close": close_time}
    print(f"Open: {open_time}, Close: {close_time}")
    return flask.jsonify(result=result)


#############

# Displaying the data
@app.route("/display")
def display_brevets():
    return flask.render_template('display_ajax.html')
#    global collection
#    if collection.count_documents({}) < 1:   # If the collection is empty, return our error
#        return flask.render_template('db_empty.html')
#    
    #Create a table of all the entries
#    table = []
#    for entrie in collection.find():
#        _id, miles, km, location, open_t, close_t = entrie.values()
#        print(km)
#        row = [miles, km, location, open_t, close_t]
#        for el in row:
#            print(el)
#        table.append(row)
#
#    return flask.render_template('display.html', table_body=table)

@app.route("/displayempty")

def display_empty():
    return flask.render_template('db_empty.html')

@app.route("/insert")
def add():
    global collection
    app.logger.debug("Got a JSON request")
    args = request.args
    print(args)
    #Check if the json is empty
    if not args:
        return flask.jsonify({ 'error': 'empty' })
    try:
        brevet = {'miles': args['miles'], 'km': args['km'], 
                  'location': args['location'], 'open_t': args['open_t'],
                  'close_t': args['close_t']}
        collection.insert_one(brevet)
    except:
        return flask.jsonify({ 'error': 'failed' })
    return flask.jsonify( {'status': 'ok'} )

@app.route("/fetch")
def fetch():
    global collection
    return_json = {}
    x = 0
    for entrie in collection.find():
        _id, miles, km, location, open_t, close_t = entrie.values()
        return_json['row'.join(str(x))] = {'miles': miles, 'km': km, 'location': location,
                                           'open_t': open_t, 'close_t': close_t}
        x+=1
    return flask.jsonify(return_json)




#Just a tester, basically just adds Sample_Data before working on the JS frontend
@app.route("/add_garbage")
def add_garbage():
    global collecton
    collection.insert_one({'miles': '6.2', 'km' : '10', 'location' : 'name',
                           'open_t' : 'Sun 1/1 0:17',
                           'close_t ': 'Sun 1/1 1:30'
                           })
    return flask.redirect('/display')



app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.debug = True
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
