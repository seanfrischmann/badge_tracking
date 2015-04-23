CREATE TABLE Employee_Data(
	Employee_Id INT PRIMARY KEY,
	Nfc_Id INT NOT NULL UNIQUE,
	Employee_Name VARCHAR(30) NOT NULL,
	Department VARCHAR(30) NOT NULL,
	Clearence_Level INT NOT NULL
	CHECK (Clearence_Level >= 0 and Clearence_Level <= 3),
	Coordinates VARCHAR(10) NOT NULL,
	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Location_History(
	Employee_Id INT,
	Coordinates VARCHAR(10) NOT NULL,
	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (Employee_Id) REFERENCES Badge_Data(Employee_Id)
);

CREATE TABLE Security_Personnel(
	Employee_Id INT,
	Username VARCHAR(30) PRIMARY KEY,
	Password VARCHAR(30) NOT NULL,
	FOREIGN KEY (Employee_Id) REFERENCES Badge_Data(Employee_Id)
);

CREATE TABLE Rooms(
	Room_Id INT PRIMARY KEY,
	Department VARCHAR(30) NOT NULL,
	Coordinates VARCHAR(10) NOT NULL
);

CREATE TABLE Employee_Access(
	Room_Id INT,
	Employee_Id INT,
	FOREIGN KEY (Employee_Id) REFERENCES Badge_Data(Employee_Id),
	FOREIGN KEY (Room_Id) REFERENCES Room_Access(Room_Id)
);

CREATE TABLE Routers(
	Id INT PRIMARY KEY,
	Coordinates VARCHAR(10) NOT NULL
);
