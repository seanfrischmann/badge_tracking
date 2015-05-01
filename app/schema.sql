CREATE TABLE Employee_Data(
	Employee_Id INT PRIMARY KEY,
	Nfc_Id VARCHAR(20) NOT NULL UNIQUE,
	Employee_Name VARCHAR(30) NOT NULL,
	Department VARCHAR(30) NOT NULL,
	Clearence_Level INT NOT NULL
	CHECK (Clearence_Level >= 0 and Clearence_Level <= 3),
	Coordinate_X INT,
	Coordinate_y INT,
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
	Room_Id VARCHAR(20) PRIMARY KEY,
	Department VARCHAR(30) NOT NULL
);

CREATE TABLE Employee_Access(
	Room_Id VARCHAR(20),
	Employee_Id INT,
	FOREIGN KEY (Employee_Id) REFERENCES Badge_Data(Employee_Id),
	FOREIGN KEY (Room_Id) REFERENCES Room_Access(Room_Id)
);

CREATE TABLE Routers(
	Id INT PRIMARY KEY,
	BSSID VARCHAR(30) UNIQUE NOT NULL,
	SSID VARCHAR(30) UNIQUE NOT NULL,
	Frequency INT NOT NULL,
	Level INT NOT NULL,
	Coordinates VARCHAR(10) NOT NULL
);

CREATE TABLE API_Tokens(
	Request_Name VARCHAR(30) PRIMARY KEY,
	Token VARCHAR(30) UNIQUE NOT NULL
);
