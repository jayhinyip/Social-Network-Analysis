# Laing O'Rourke Social Network Project
This is an improvement on the previous prototype developed by the 2019 ENGG4064 JFC Team.

Team Members:

 - Tony Xiao
 - Jay Hin Yip
 - Rashid AL-Naamani
 - Kevin Wang
 - William Boustred

# Update 2019-2020
Improvements to be made
  - eveness.py: account for multiple receivers from one sender
  - makeNetwork.py: check the "Catch for sending to self" if it works, if len(temp)<2

# Update 2020
Web Application for social network analysis. 

Python Flask is required and a flask server can be made by running flask_server.py and then accessed at 127.0.0.1:5000/ in your browser.

The application is then used by making searches, the searches must be character correct.

  - Employees of Interest: Top Collaborators, knowledge brokers, Isolated individuals 
  - Project Network: Network visualization tool
  - Employee Lookup: Seach list of employees of that particular branch
  - Logout: Logout of portal
  
Input file is SNA_Data.xlsx and can be replaced providing that the filename and column headings remain the same.

Search time is the greatest problem with the application and some searches that involve a large number of offices or cities take a large time to perform the analysis.

# User Manual
Software: Python, mySQL

Steps:

To establish SQL database:-
1. Create databases

CREATE DATABASE IF NOT EXISTS pythonlogin DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE pythonlogin;accountsaccounts

CREATE TABLE IF NOT EXISTS accounts (
	id int(11) NOT NULL AUTO_INCREMENT,
  	username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
  	email varchar(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO accounts (id, username, password, email, Branch) VALUES (1, 'test', 'test', 'test@test.com', 'north_sydney_mount_street');

CREATE DATABASE testdatabase

2. Run SQLBegin.py
3. Run NWL Database.py
4. Alter table simpleID column name "CloseCent" to "ClosenessCent"
5. Run impactrecommenderfix.py
6. Run BranchDatabaseStart.py

To establish server:-

7. Run flask_servernewtry.py
