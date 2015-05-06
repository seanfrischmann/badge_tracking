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

def checkApiToken(data):
	token = data['database'].execute(
			"SELECT Token FROM API_Tokens WHERE"+
			" Request_Name = ?", [data['Request_Name']])
	token = [row[0] for row in token.fetchall()]
	if token[0] == data['Token']:
		return True
	return False

def verifyLogin(data):
	ret = False
	dpmt = data['database'].execute(
			"SELECT CASE WHEN EXISTS ("+
			" SELECT * FROM Security_Personnel WHERE"+
			" Username = ? AND Password = ?)"+
			" THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
			, [data['username'],data['password']])
	dpmt = [row[0] for row in dpmt.fetchall()]
	if bool(dpmt[0]):
		ret = True
	if (data['username'] == data['user_conf']) and (data['password'] == data['pass_conf']):
		ret = True
	return ret

def checkEmployeeAccess(data):
	dpmt = data['database'].execute(
			"SELECT CASE WHEN EXISTS ("+
			" SELECT * FROM Employee_Access WHERE"+
			" Employee_Id = ? AND Room_Id = ?)"+
			" THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
			, [data['Employee_Id'],data['Room_Id']])
	dpmt = [row[0] for row in dpmt.fetchall()]
	return bool(dpmt[0])

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

def postEmployeeAcess(data):
	if data['Department'] == 'security':
		data['database'].execute("INSERT INTO Employee_Access "
				+"(Room_Id,Employee_Id) SELECT R.Room_Id, E.Employee_Id "
				+"FROM Employee_Data E JOIN Rooms R on "
				+"E.Employee_Id = ?" , [data['Employee_Id']])
	else:
		data['database'].execute("INSERT INTO Employee_Access "
				+"(Room_Id,Employee_Id) SELECT R.Room_Id, E.Employee_Id "
				+"FROM Employee_Data E JOIN Rooms R on "
				+"R.Department = ? and E.Employee_Id = ?" , [data['Department'],data['Employee_Id']])
	data['database'].commit()

def deleteEmployeeAccess(data):
	data['database'].execute(
			"DELETE FROM Employee_Access WHERE "+
			"Employee_Id = ?", [data['Employee_Id']])
	data['database'].commit()

def delete(data):
	if checkData(data):
		return 'Please fill out all fields'
	try:
		message = 'Employee was successfully removed'
		if checkEmployee(data, 'delete'):
			data['database'].execute(
					"DELETE FROM Employee_Data WHERE Employee_Name = ?"+
					" AND Employee_Id = ?", [data['Employee_Name'], data['Employee_Id']])
			data['database'].execute(
					"DELETE FROM Security_Personnel WHERE Username = ?"+
					" AND Employee_Id = ?", [data['Employee_Name'], data['Employee_Id']])
			data['database'].commit()
			deleteEmployeeAccess(data)
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
			data['database'].execute("INSERT INTO Employee_Data "
			+"(Employee_Name, Employee_Id, Nfc_Id, Department, Clearence_Level) "
			+"VALUES (?,?,?,?,?)", 
					[data['Employee_Name'], data['Employee_Id'], data['Nfc_Id'], 
						data['Department'], data['Clearence_Level']])
			if data['Department'] == 'security':
				data['database'].execute("INSERT INTO Security_Personnel "
				+"(Employee_Id, Username, Password) "
				+"VALUES (?,?,?)", 
						[data['Employee_Id'], data['Employee_Name'], 
							data['Password']])
			data['database'].commit()
			postEmployeeAcess(data)
		return message
	except:
		return 'There was a system error, Employee was not added'

def update(data):
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
			deleteEmployeeAccess(data)
			postEmployeeAcess(data)
		else:
			message = 'Employee does not exists'
		return message
	except:
		return 'There was a system error, Employee was not added'

def getEmployeeList(database):
	cur = database.execute(
			"SELECT Employee_Name, Employee_Id, Department, Coordinate_X, Coordinate_Y FROM Employee_Data")
	empList = [(row[0], row[1], row[2], row[3], row[4]) for row in cur.fetchall()]
	return empList

def getEmployee(data):
	cur = data['database'].execute(
			"SELECT Employee_Name, Employee_Id, Department, Coordinate_X, Coordinate_Y FROM Employee_Data "
			+"WHERE Employee_Id = ?", [data['Employee_Id']])
	empList = [(row[0], row[1], row[2], row[3], row[4]) for row in cur.fetchall()]
	return empList

def getEmployeeLocation(data):
	cur = data['database'].execute(
			"SELECT Coordinate_X, Coordinate_Y FROM Employee_Data WHERE "
			+"Employee_Id = ?",
			[data['Employee_Id']])
	empLocation = [[row[0],row[1]] for row in cur.fetchall()] 
	empLocation = empLocation[0]
	return empLocation
	
def updateEmployeeLocation(data):
	data['database'].execute(
			"UPDATE Employee_Data SET Coordinate_X = ?, Coordinate_Y = ?, "
			+"Timestamp = CURRENT_TIMESTAMP "
			+"WHERE Employee_Id = ?",
			[data['Coordinate_X'], data['Coordinate_Y'],data['Employee_Id']])
	data['database'].commit()

