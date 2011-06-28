import sqlite3
con = sqlite3.connect('soquestions.db') # Warning: This file is created in the current directory
con.execute("CREATE TABLE so (id INTEGER PRIMARY KEY, questionid INTEGER, numberofanswers INTEGER)")
con.commit()
