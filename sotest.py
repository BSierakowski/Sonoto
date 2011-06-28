import stackexchange 
import sqlite3
import os.path
import create_db

site = stackexchange.Site("api.stackoverflow.com")

user = site.user(637160)
allquestions = user.questions.fetch()

#DB Check
if os.path.isfile("soquestions.db") == False:
    print "Creating soquestions database."
    con = sqlite3.connect('soquestions.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE so (questionid INTEGER, numberofanswers INTEGER)")
    con.commit()
else:
    print "Database exists, checking number of questions."


    
numberofquestions = len(allquestions)
print "number of questions for %s on SO: %d" % (user.display_name, numberofquestions)

dbquestioncount = 0

conn = sqlite3.connect('soquestions.db')
c = conn.cursor()
c.execute('select * from so')
for rows in c:
    dbquestioncount += 1
    
print "number of questions for user in DB: %d" % (dbquestioncount)

count = 0 

if numberofquestions == dbquestioncount:
    print "No Changes!"
elif dbquestioncount > allquestions:
    print "There's a problem!"
elif dbquestioncount < allquestions:
    conn = sqlite3.connect('soquestions.db')
    c = conn.cursor()

    for entry in allquestions:
        questionid = entry.id
        answers = site.question(questionid).answers
        numberofanswers = len(answers)
        
        print "Inserting question ID: %d" % questionid
        print "Number of answers: %d" % numberofanswers
        print " "
        c.execute("REPLACE INTO so (questionid,numberofanswers) VALUES (?,?)", (questionid,numberofanswers))
        conn.commit()
    count += 1    
    conn.close()

else:
    print "Well that's not supposed to happen." 



