# ===========================================================================
# +++badge_tracking.py+++|
# _______________________|
#
# Sean Frischmann
# Badge Tracking App
# ===========================================================================

# Imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash


#create app
app = Flask(__name__)

# Configuration
app.config.from_object('config')
#app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add_employee')
def add_employee():
	return render_template('add_employee.html')

@app.route('/remove_update')
def remove_update():
	return render_template('remove_update.html')

@app.route('/update_employee', methods=['POST'])
def update_employee():
	if not session.get('logged_in'):
		abort(401)
	try:
		flash('Employee was successfully updated')
	except ValueError:
		flash('There was a system error, Employee was not updated')
	return redirect(url_for('index'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
	if not session.get('logged_in'):
		abort(401)
	try:
		g.db.execute("DELETE FROM Employee_Data WHERE Employee_Name = '"+request.form['Employee_Name']+"'")
		g.db.commit()
		flash('Employee was successfully removed')
	except ValueError:
		flash('There was a system error, Employee was not removed')
	return redirect(url_for('index'))

@app.route('/post_employee', methods=['POST'])
def post_employee():
	if not session.get('logged_in'):
		abort(401)
	try:
		g.db.execute("insert into Employee_Data (Employee_Name, Employee_Id, Nfc_Id, Department, Clearence_Level, Coordinates ) values (?,?,?,?,?,'0')", 
				[request.form['Employee_Name'], request.form['Employee_Id'], request.form['Nfc_Id'], request.form['Department'], request.form['Clearence_Level']])
		g.db.commit()
		flash('New entry was successfully posted')
	except ValueError:
		flash('There was a system error, Employee was not added')
	return redirect(url_for('index'))
'''
@app.route('/request_position', methods=['POST'])
def request_position():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, ingredients, review) values (?,?,?)', 
			[request.form['title'], request.form['ingredients'], request.form['review']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('request_position'))
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('index'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()
'''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello!"

'''
