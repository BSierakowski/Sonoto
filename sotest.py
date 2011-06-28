import stackexchange 
import sqlite3

site = stackexchange.Site("api.stackoverflow.com")

user = site.user(637160)
allquestions = user.questions.fetch()


count = 0 

for entry in allquestions:
    questionid = entry.id
    answers = site.question(questionid).answers
    numberofanswers = len(answers)
    conn = sqlite3.connect('soquestions.db')
    c = conn.cursor()
    c.execute("INSERT INTO so (questionid,numberofanswers) VALUES (?,?)", (questionid,numberofanswers))
    conn.commit()
    conn.close()
    print "Current count: %d" % count
    print "Current Question ID: %d" % questionid
    print "Number of answers: %d" % numberofanswers
    print " "
     
    count += 1 
