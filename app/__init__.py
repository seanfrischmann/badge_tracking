# ===========================================================================
# +++badge_tracking.py+++|
# _______________________|
#
# Sean Frischmann
# Badge Tracking App
# ===========================================================================

# Imports
import sqlite3
import app.db_queries as query
import app.coordinates as coor
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

@app.route('/get_employeeList')
def get_employeeList():
	return query.getEmployeeList(g.db)

@app.route('/get_employee/<Employee_Id>')
def get_employee(Employee_Id):
	data = {
			'database':g.db,
			'Employee_Id':Employee_Id}
	flash(query.getEmployee(data))
	return redirect(url_for('index'))

@app.route('/add_employee')
def add_employee():
	return render_template('add_employee.html')

@app.route('/remove_update')
def remove_update():
	return render_template('remove_update.html')

@app.route('/test_scan_nfc')
def test_scan_nfc():
	return render_template('test_scan_nfc.html')

@app.route('/post_nfcScan', methods=['POST'])
def post_nfcScan():
	data = {'database':g.db,
			'Token':request.form['Token'],
			'Request_Name':'Nfc_Scan',
			'Employee_Id':request.form['Employee_Id'], 
			'Room_Id':request.form['Room_Id']}
	if not query.checkApiToken(data):
		abort(401)
	check = query.checkEmployeeAccess(data)
	if check:
		query.updateEmployeeLocation(data)
	return check

@app.route('/post_wifiScan', methods=['POST'])
def post_wifiScan():
	data = {'database':g.db,
			'Token':request.form['Token'],
			'Request_Name':'Wifi_Scan',
			'Employee_Id':request.form['Employee_Id'], 
			'trimmedResults':request.form['trimmedResults']}
	if not query.checkApiToken(data):
		abort(401)
	data['Coordinates'] = coor.coordinates(data['trimmedResults'])
	query.updateEmployeeLocation(data)

@app.route('/update_employee', methods=['POST'])
def update_employee():
	if not session.get('logged_in'):
		abort(401)
	data = {'database':g.db,
			'Employee_Name':request.form['Employee_Name'].upper(), 
			'Employee_Id':request.form['Employee_Id'], 
			'Nfc_Id':request.form['Nfc_Id'], 
			'Department':request.form['Department'], 
			'Clearence_Level':request.form['Clearence_Level']}
	flash(query.update(data))
	return redirect(url_for('index'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
	if not session.get('logged_in'):
		abort(401)
	data = {'database':g.db,
			'Employee_Name':request.form['Employee_Name'].upper(), 
			'Employee_Id':request.form['Employee_Id']}
	flash(query.delete(data))
	return redirect(url_for('index'))

@app.route('/post_employee', methods=['POST'])
def post_employee():
	if not session.get('logged_in'):
		abort(401)
	data = {'database':g.db,
			'Employee_Name':request.form['Employee_Name'].upper(), 
			'Employee_Id':request.form['Employee_Id'], 
			'Nfc_Id':request.form['Nfc_Id'], 
			'Department':request.form['Department'], 
			'Clearence_Level':request.form['Clearence_Level']}
	flash(query.post(data))
	return redirect(url_for('index'))

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
