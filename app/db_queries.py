# ===========================================================================
# +++db_querries.py+++|
# _______________________|
#
# Sean Frischmann
# Badge Tracking App
# ===========================================================================



def checkData(data):
	for value in data:
		if value is '':
			return True
	return False

def checkEmployee(data, flag):
	if (flag is 'update') or (flag is 'delete'):
		emp_id = data['database'].execute(
				"SELECT CASE WHEN EXISTS ("+
				" SELECT * FROM Employee_Data WHERE"+
				" Employee_Name = ? AND Employee_Id = ?)"+
				" THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
				, [data['Employee_Name'], data['Employee_Id']])
	else:
		emp_id = data['database'].execute(
				"SELECT CASE WHEN EXISTS ("+
				" SELECT Employee_Id FROM Employee_Data WHERE"+
				" Employee_Id = ?)"+
				" THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
				, [data['Employee_Id']])
	emp_id = [row[0] for row in emp_id.fetchall()]
	return bool(emp_id[0])

def delete(data):
	if checkData(data):
		return 'Please fill out all fields'
	try:
		message = 'Employee was successfully removed'
		if checkEmployee(data, 'delete'):
			data['database'].execute(
					"DELETE FROM Employee_Data WHERE Employee_Name = ?"+
					" AND Employee_Id = ?", [data['Employee_Name'], data['Employee_Id']])
			data['database'].commit()
		else:
			message = 'Employee does not exist'
		return message
	except:
		return 'There was a system error, Employee was not removed'

def post(data):
	if checkData(data):
		return 'Please fill out all fields'
	try:
		message = 'Employee was successfully added'
		if checkEmployee(data, 'post'):
			message = 'Employee Id already exists'
		else:
			data['database'].execute("insert into Employee_Data "
			+"(Employee_Name, Employee_Id, Nfc_Id, Department, Clearence_Level, Coordinates ) "
			+"values (?,?,?,?,?,'0')", 
					[data['Employee_Name'], data['Employee_Id'], data['Nfc_Id'], 
						data['Department'], data['Clearence_Level']])
			data['database'].commit()
		return message
	except:
		return 'There was a system error, Employee was not added'

def update(data):
	'''
	test = {
			'Employee_Name':data['Employee_Name'],
			'Employee_Id':data['Employee_Id'],
			'database':data['database'],
			'Coordinates':10}
	updateEmployeeLocation(test)
	'''
	try:
		message = 'Employee was successfully updated'
		if checkEmployee(data, 'update'):
			stmt = 'SET '
			changes = []
			for row in data:
				if (row is not 'database') and (row is not 'Employee_Id'
						) and (row is not 'Employee_Name'):
					if data[row] is not '':
						changes.append(row+'='+"'"+data[row]+"'")
			i = 0
			while i < len(changes):
				stmt += changes[i]
				if i is not (len(changes)-1):
					stmt += ', '
				i += 1
			data['database'].execute("UPDATE Employee_Data "
					+stmt+" WHERE Employee_Name = ? AND Employee_Id = ?",
					[data['Employee_Name'], data['Employee_Id']])
			data['database'].commit()
		else:
			message = 'Employee does not exists'
		return message
	except:
		return 'There was a system error, Employee was not added'

def getEmployeeList(database):
	cur = database.execute("SELECT Employee_Name, Employee_Id, Department FROM Employee_Data")
	empList = [(row[0], row[1], row[2]) for row in cur.fetchall()]
	return empList

def getEmployee(data):
	cur = data['database'].execute(
			"SELECT Employee_Name, Employee_Id, Department FROM Employee_Data "
			+"WHERE Employee_Id = ?", [data['Employee_Id']])
	empList = [(row[0], row[1], row[2]) for row in cur.fetchall()]
	return empList

def getEmployeeLocation(data):
	cur = data['database'].execute(
			"SELECT Coordinates FROM Employee_Data WHERE "
			+"Employee_Name = ? AND Employee_Id = ?",
			[data['Employee_Name'],data['Employee_Id']])
	empLocation = [row[0] for row in cur.fetchall()] 
	return empLocation
	
def updateEmployeeLocation(data):
	data['database'].execute(
			"UPDATE Employee_Data SET Coordinates = ?, Timestamp = CURRENT_TIMESTAMP "
			+"WHERE Employee_Name = ? AND Employee_Id = ?",
			[data['Coordinates'],data['Employee_Name'],data['Employee_Id']])
	data['database'].commit()

