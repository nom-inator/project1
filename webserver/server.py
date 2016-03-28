#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, session, flash, jsonify
import forecastio # weather api
from datetime import datetime
import operator

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
weather_api_key = '97fcdbefb9c4d2b4fbb6c6f2121ea33e'

#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://localhost/nominator"
#DATABASEURI = "postgresql://cw2952:EZANNW@w4111db.eastus.cloudapp.azure.com/cw2952"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")

#
# END SQLITE SETUP CODE
#


engine.execute("""CREATE TABLE IF NOT EXISTS users (
  id serial,
  pass text,
  name text
);""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  

  #context['users'] = users
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  if 'username' in session:

      cursor = g.conn.execute("SELECT * FROM Restaurant r;" )
      restaurant = cursor.fetchall()

      username = session['username']
      cursor = g.conn.execute("SELECT * FROM Users WHERE uid = %s;", username)
      #cursor = g.conn.execute("SELECT * FROM Users ;" )      
      users = cursor.fetchone()
      if users == None:
        return render_template("login.html")

      cursor = g.conn.execute("SELECT listid FROM favouriteslist WHERE uid = %s;", username)
      listid = cursor.fetchone()['listid']

      cursor = g.conn.execute("SELECT rid FROM restaurantoflist WHERE listid = %s;", listid)
      favs = []
      for result in cursor:
        res = g.conn.execute("SELECT * FROM restaurant r, Address a WHERE r.rid = %s AND r.aid = a.aid;", result['rid'])
        favs.append(res.fetchone())
        #users.append(result['rid'])  
      cursor.close()  

      return render_template("index.html", username = username, users = users, listid = listid, favs = favs, restaurant=restaurant)

  return render_template("login.html")


@app.route('/signout')
def signout():
  if 'username' in session:
    pass
    session.pop('username', None)
    #flash('You were logged out')

  return redirect('/')   

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/restaurant')
def restaurant():
  rid = request.args.get('rid')
  display_directions = 0
  if rid != None:
    cursor = g.conn.execute("SELECT * FROM Restaurant r, Address a WHERE r.rid = %s AND r.aid = a.aid;" , rid)
    display_directions = 1
    #restaurant = cursor.fetchone()
  else:  
    cursor = g.conn.execute("SELECT * FROM Restaurant r, Address a WHERE r.aid = a.aid;")
  restaurant = cursor.fetchall()
  cursor.close()  
  return render_template("restaurant.html", restaurant = restaurant, display_directions=display_directions)  


@app.route('/add_new_user', methods=['POST'])
def add_new_user():
  username = request.form['username']
  password = request.form['password']
  name = request.form['name']

  cursor = g.conn.execute("SELECT * FROM users WHERE uid = %s;", (username))
  if cursor.fetchone() != None:
    return "user already exists"

  cursor = g.conn.execute("SELECT COUNT(*) FROM Users;" )
  lid = "l"+str(cursor.fetchone()[0]+1)
  # because of foreign key constraint, insert with uid = NULL and update table after new user is added into "Users" table
  g.conn.execute("""INSERT INTO user_location VALUES (%s, NULL , %s, %s);""" , (lid, 0, 0)) 
  g.conn.execute("""INSERT INTO Users VALUES (%s, %s, %s, %s);""" , (username, name, lid, password))
  g.conn.execute("""UPDATE user_location SET uid = %s WHERE lid = %s;""" , (username, lid)) 

  cursor = g.conn.execute("SELECT COUNT(*) FROM favouriteslist;" )
  listid = "list"+str(cursor.fetchone()[0]+1)
  g.conn.execute("""INSERT INTO favouriteslist VALUES (%s, %s);""" , (listid, username))

  cursor.close()

  session['username'] = username
  return redirect('/') 

@app.route('/add_fav')
def add_fav():
  rid = request.args.get('rid')
  username = session['username']
  if rid != None and username != None:
    cursor = g.conn.execute("""SELECT listid FROM favouriteslist WHERE uid = %s;""" , username)  
    listid = cursor.fetchone()['listid']
    g.conn.execute("""INSERT INTO restaurantoflist VALUES (%s, %s);""" , (rid, listid))
    cursor.close()
  return redirect('/')   

@app.route('/del_fav')
def del_fav():
  rid = request.args.get('rid')
  username = session['username']
  if rid != None and username != None:
    cursor = g.conn.execute("""SELECT listid FROM favouriteslist WHERE uid = %s;""" , username)  
    listid = cursor.fetchone()['listid']
    g.conn.execute("""DELETE FROM restaurantoflist WHERE rid =%s AND listid = %s;""" , (rid, listid))
    cursor.close()
  return redirect('/')   

@app.route('/update_coordinate', methods=['POST'])
def update_coordinate():
  jlat = request.form['lat']
  jlon = request.form['lon']
  g.conn.execute("""UPDATE user_location SET lat = %s, lng = %s  WHERE uid = %s;""" , (jlat, jlon,session['username']))
  cursor.close()
  return jsonify(lat = jlat, lon = jlon)
  

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      cursor = g.conn.execute("SELECT * FROM users WHERE uid = %s AND passwd = %s;" , (username, password))
      if cursor.fetchone() != None:
        session['username'] = username
        cursor.close()
        return redirect("/")
      cursor.close()
      return render_template("login.html")
    else:   
      return redirect("/")

# get location
def get_current_location():
    cursor = g.conn.execute("SELECT * FROM user_location WHERE uid = %s;", session['username'])
    return cursor.fetchone()

# get weather
def get_current_weather(location):
    forecast = forecastio.load_forecast(weather_api_key, location['lat'], location['lng'])
    current_conditions = forecast.currently().icon
    snow_likes = ['snow','sleet','hail']

    # default weather is clear
    if current_conditions=='rain':
      return 'rainy'
    elif any(current_conditions==snow_like for snow_like in snow_likes):
      return 'snowy'
    elif 'cloudy' in current_conditions or current_conditions=='fog':
      return 'cloudy'
    
    return 'clear'

# get meal
def get_current_meal():
    current_hour = datetime.now().hour
    if current_hour >= 12 and current_hour <= 17:
      return 'lunch'
    elif current_hour < 12 or current_hour < 3:
      return 'breakfast'
    else:
      return 'dinner'

def initialise_score_dict(default_score=0.0):

    cursor = g.conn.execute("SELECT DISTINCT rid FROM restaurant;")
    all_rids = [result['rid'] for result in cursor.fetchall()]
    return dict(zip(all_rids,[default_score]*len(all_rids)))

# calculate wait_time_score
def calculate_wait_time_score(day, weather, meal, weight):

    scores = initialise_score_dict()

    cursor = g.conn.execute("SELECT cid FROM condition WHERE day_of_week=%s AND weather=%s AND time=%s;" , (day, weather, meal))
    cond = cursor.fetchone()
    if cond != None:

      cid = cond['cid']
      cursor = g.conn.execute("SELECT * FROM visit WHERE cid='%s';" % cid)
      # cursor = g.conn.execute("SELECT * FROM visit LIMIT 10")
      
      if cursor.fetchone() != None:

        cursor = g.conn.execute("SELECT * FROM visit WHERE cid='%s';" % cid)
        matching_data = cursor.fetchall()
        rids = [visit_data['rid'] for visit_data in matching_data]
        
        visits = [float(visit_data['count']) for visit_data in matching_data]
        min_visit = min(visits)
        max_visit = max(visits)
        norm_vists = [ ( visit - min_visit ) / ( max_visit - min_visit ) for visit in visits ]
        
        for i in xrange(len(rids)):
          scores[rids[i]] = ( weight - 50.0 ) / 50.0 * norm_vists[i]
    
    return scores

# calculate distance_score
def calculate_distance_score(location, weight):

    scores = initialise_score_dict()

    cursor = g.conn.execute("SELECT rid, lat, lng FROM address;")

    if cursor.fetchone() != None:

      cursor = g.conn.execute("SELECT rid, lat, lng FROM address;")
      restaurants = cursor.fetchall()
      rids = [ rest['rid'] for rest in restaurants ]

      distances = [ ((location['lat'] - rlocation['lat'])**2 + (location['lng'] - rlocation['lng'])**2) for rlocation in restaurants ]
      min_distance = min(distances)
      max_distance = max(distances)
      norm_distances = [ ( dist - min_distance ) / ( max_distance - min_distance ) for dist in distances ]

      for i in xrange(len(rids)):
        scores[rids[i]] = ( weight / 100.0 ) * float(norm_distances[i])

      return scores


# calculate novelty_score
def calculate_novelty_score(weight):

    scores = initialise_score_dict(-1.0 * (weight-50.0) / 50.0)

    cursor = g.conn.execute("SELECT listid FROM favouriteslist WHERE uid =%s;" , (session['username']) )

    listid = cursor.fetchone()['listid']

    cursor = g.conn.execute("SELECT rid FROM restaurantoflist WHERE listid = %s;" , (listid))

    if cursor.fetchone() != None:
      cursor = g.conn.execute("SELECT rid FROM restaurantoflist WHERE listid = %s;" , (listid))
      fav_rids = [row['rid'] for row in cursor.fetchall()]
      for i in xrange(len(fav_rids)):
          scores[fav_rids[i]] = scores[fav_rids[i]] * -1.0

    return scores

@app.route('/nominate_now', methods=['POST'])
def nominate_now():
    
    wait_time_weight = float(request.form['wait_time'])
    distance_weight = float(request.form['distance'])
    novelty_weight = float(request.form['novelty'])

    current_location = get_current_location()
    current_weather = get_current_weather(current_location)
    current_meal = get_current_meal()
    current_day = datetime.today().weekday() + 1

    wait_time_score = calculate_wait_time_score(current_day, current_weather, current_meal, wait_time_weight)
    distance_score = calculate_distance_score(current_location, distance_weight)
    novelty_score = calculate_novelty_score(novelty_weight)

    # calculate overall_score
    overall_score = initialise_score_dict()
    for key, value in overall_score.iteritems():
      overall_score[key] += wait_time_score[key] + distance_score[key] + novelty_score[key]

    # determine rankings
    rankings = sorted(overall_score.items(), key=operator.itemgetter(1))
    rid_list = [ ranking[0] for ranking in rankings ]
    ranked_restaurants = [ g.conn.execute("SELECT * FROM Restaurant r, Address a WHERE r.rid = '%s'AND r.aid = a.aid;" % (rid) ).fetchone() for rid in rid_list ]

    cursor.close()
    return render_template("nominate-now.html", ranked_restaurants=ranked_restaurants)

@app.route('/nominate_later', methods=['POST'])
def nominate_later():

    selected_rid = request.form['select_restaurant']
    rankings = []

    cursor = g.conn.execute("SELECT rname FROM restaurant WHERE rid=%s;" , (selected_rid) )
    restaurant_name = cursor.fetchone()

    cursor = g.conn.execute("SELECT day_of_week, time FROM visit AS V, condition AS C WHERE V.rid =%s AND C.cid=V.cid ORDER BY V.count ASC;" , (selected_rid) )
    if cursor.fetchone() != None:
      cursor = g.conn.execute("SELECT day_of_week, time FROM visit AS V, condition AS C WHERE V.rid =%s AND C.cid=V.cid ORDER BY V.count ASC;" , (selected_rid) )
      rankings = cursor.fetchall()

    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    rankings = [ (weekdays[ranking['day_of_week'] - 1], ranking['time']) for ranking in rankings ]

    cursor.close()
    return render_template("nominate-later.html", rankings=rankings, restaurant_name=restaurant_name)

if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    


  run()
