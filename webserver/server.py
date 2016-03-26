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

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
      cursor = g.conn.execute("SELECT * FROM Users WHERE uid = '%s';" % (username))
      #cursor = g.conn.execute("SELECT * FROM Users ;" )      
      users = cursor.fetchone()
      if users == None:
        return render_template("login.html")

      cursor = g.conn.execute("SELECT listid FROM favouriteslist WHERE uid = '%s';" % (username))
      listid = cursor.fetchone()['listid']

      cursor = g.conn.execute("SELECT rid FROM restaurantoflist WHERE listid = '%s';" % (listid))
      favs = []
      for result in cursor:
        res = g.conn.execute("SELECT * FROM restaurant r, Address a WHERE r.rid = '%s' AND r.aid = a.aid;" % (result['rid']))
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
  if rid != None:
    cursor = g.conn.execute("SELECT * FROM Restaurant r, Address a WHERE r.rid = '%s'AND r.aid = a.aid;" % rid)
    #restaurant = cursor.fetchone()
  else:  
    cursor = g.conn.execute("SELECT * FROM Restaurant r, Address a WHERE r.aid = a.aid;")
  restaurant = cursor.fetchall()
  cursor.close()  
  return render_template("restaurant.html", restaurant = restaurant)  


@app.route('/add_new_user', methods=['POST'])
def add_new_user():
  username = request.form['username']
  password = request.form['password']
  name = request.form['name']

  cursor = g.conn.execute("SELECT COUNT(*) FROM Users;" )
  lid = "l"+str(cursor.fetchone()[0]+1)
  # because of foreign key constraint, insert with uid = NULL and update table after new user is added into "Users" table
  g.conn.execute("""INSERT INTO user_location VALUES ('%s', NULL , '%s', '%s');""" % (lid, 0, 0)) 
  g.conn.execute("""INSERT INTO Users VALUES ('%s', '%s', '%s');""" % (username, name, lid))
  g.conn.execute("""UPDATE user_location SET uid = '%s' WHERE lid = '%s';""" % (username, lid)) 

  cursor = g.conn.execute("SELECT COUNT(*) FROM favouriteslist;" )
  listid = "list"+str(cursor.fetchone()[0]+1)
  g.conn.execute("""INSERT INTO favouriteslist VALUES ('%s', '%s');""" % (listid, username))

  cursor.close()

  session['username'] = username
  return redirect('/') 

@app.route('/add_fav')
def add_fav():
  rid = request.args.get('rid')
  username = session['username']
  if rid != None and username != None:
    cursor = g.conn.execute("""SELECT listid FROM favouriteslist WHERE uid = '%s';""" % username)  
    listid = cursor.fetchone()['listid']
    g.conn.execute("""INSERT INTO restaurantoflist VALUES ('%s', '%s');""" % (rid, listid))
    cursor.close()
  return redirect('/')   

@app.route('/del_fav')
def del_fav():
  rid = request.args.get('rid')
  username = session['username']
  if rid != None and username != None:
    cursor = g.conn.execute("""SELECT listid FROM favouriteslist WHERE uid = '%s';""" % username)  
    listid = cursor.fetchone()['listid']
    g.conn.execute("""DELETE FROM restaurantoflist WHERE rid ='%s' AND listid = '%s';""" % (rid, listid))
  return redirect('/')   

@app.route('/update_coordinate', methods=['POST'])
def update_coordinate():
  jlat = request.form['lat']
  jlon = request.form['lon']
  g.conn.execute("""UPDATE user_location SET lat = '%s', lng = '%s'  WHERE uid = '%s';""" % (jlat, jlon,session['username']))
  return jsonify(lat = jlat, lon = jlon)
  

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      cursor = g.conn.execute("SELECT * FROM users WHERE uid = '%s';" % (username))
      if cursor.fetchone() != None:
        session['username'] = username
        return redirect("/")
  
      return render_template("login.html")
    else:   
      return redirect("/")

@app.route('/nominate_now', methods=['POST'])
def nominate_now():
    wait_time = request.form['wait_time']
    distance = request.form['distance']
    novelty = request.form['novelty']

    return render_template("nominate-now.html", wait_time=wait_time, distance=distance, novelty=novelty)

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
