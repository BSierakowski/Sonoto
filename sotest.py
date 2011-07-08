import stackexchange 
import sqlite3
import os.path

site = stackexchange.Site("api.stackoverflow.com")

user = site.user(637160)
all_questions_from_so_api_list = user.questions.fetch()

#DB Check
if os.path.isfile("soquestions.db") == False:
    print "Creating soquestions database."
    con = sqlite3.connect('soquestions.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE so (questionid INTEGER, numberofanswers INTEGER)")
    con.commit()
else:
    print "Database exists, checking number of questions."


    
number_questions_so_api = len(all_questions_from_so_api_list)
print "number of questions for %s on SO: %d" % (user.display_name, number_questions_so_api)

number_questions_db = 0

conn = sqlite3.connect('soquestions.db')
c = conn.cursor()
c.execute('select * from so')
for rows in c:
    number_questions_db += 1
    
print "number of questions for user in DB: %d" % (number_questions_db)

if number_questions_so_api == number_questions_db:
    print "No Changes!"
elif number_questions_db > number_questions_so_api:
    print "There's a problem!"
elif number_questions_db < number_questions_so_api:
    all_db_question_ids = []
    number_of_answers_db = []
    all_api_question_ids = []
    number_of_answers_api = []
    missing_questions = []

    for db_question_ids in c.execute('SELECT questionid FROM so').fetchall():
        all_db_question_ids.append(db_question_ids[0])

    for each_answer in all_db_question_ids:
        number_of_answers_db.append(len(site.question(each_answer).answers))

    for entry in all_questions_from_so_api_list:
        all_api_question_ids.append(entry.id)

    for each_answer in all_api_question_ids:
        number_of_answers_api.append(len(site.question(each_answer).answers))

    db_tuple = list(zip(all_db_question_ids,number_of_answers_db))
    api_tuple = list(zip(all_api_question_ids,number_of_answers_api))

    missing_questions = list(set(api_tuple) - set(db_tuple))

    for ids in missing_questions:
        print "Inserting question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("INSERT INTO so (questionid,numberofanswers) VALUES (?,?)", (ids[0],ids[1]))           
     
    conn.commit()
    conn.close()

else:
    print "Well that's not supposed to happen." 



