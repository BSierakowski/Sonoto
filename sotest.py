import stackexchange 
import sqlite3
import os.path

print "Configuring SO API values."
print " "

# StackOverflow API config
site = stackexchange.Site("api.stackoverflow.com")
user = site.user(637160)

print "Checking for and creating DB values."
print " "

#DB Check
if os.path.isfile("soquestions.db") == False:
    print "Creating soquestions database."
    print " "
    con = sqlite3.connect('soquestions.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE so (questionid INTEGER, numberofanswers INTEGER)")
    con.commit()
else:
    print "Database exists, checking number of questions."
    print " "

# DB config
number_questions_db = 0
conn = sqlite3.connect('soquestions.db')
c = conn.cursor()
c.execute('select * from so')
for rows in c:
    number_questions_db += 1

all_db_question_ids = [db_question_ids[0] for db_question_ids in c.execute('SELECT questionid FROM so').fetchall()]
number_of_answers_db = [number_answers_db[0] for number_answers_db in c.execute('SELECT numberofanswers FROM so').fetchall()]
total_number_answers_db = sum(number_of_answers_db)
db_tuple = list(zip(all_db_question_ids,number_of_answers_db))

print "Creating API values."
print " "

# API Values
all_questions_from_so_api_list = user.questions.fetch()
number_questions_so_api = len(all_questions_from_so_api_list)
all_api_question_ids = [entry.id for entry in all_questions_from_so_api_list]
number_of_answers_api = [len(site.question(each_answer).answers) for each_answer in all_api_question_ids]
total_number_answers_api = sum(number_of_answers_api)
api_tuple = list(zip(all_api_question_ids,number_of_answers_api))

# Status!
print "Current Status:"
print "number of questions for %s on SO: %d" % (user.display_name, number_questions_so_api)    
print "number of questions for user in DB: %d" % (number_questions_db)
print " "

# Check for new Questions
if number_questions_so_api == number_questions_db:
    print "No new questions!"
    print " "
elif number_questions_db > number_questions_so_api:
    print "Deleting Questions:"
    print "-------------------"
    print " "

    missing_questions = list(set(db_tuple) - set(api_tuple))
         
    for ids in missing_questions:
        print "Deleting question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("DELETE FROM so WHERE questionid = ?", (ids[0], ))
        conn.commit()
    
elif number_questions_db < number_questions_so_api:
    print "Adding Questions:"
    print "-----------------"
    print " "
       
    missing_questions = list(set(api_tuple) - set(db_tuple))
     
    for ids in missing_questions:
        print "Inserting question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("INSERT INTO so (questionid,numberofanswers) VALUES (?,?)", (ids[0],ids[1]))           
        conn.commit()
      
        
# Check for new Answers - if total number of answers are higher, find higher value and replace
print total_number_answers_api
print total_number_answers_db

if total_number_answers_api == total_number_answers_db:
    print "No new answers!"
    print " "
elif total_number_answers_db > total_number_answers_api:
    print "Deleting Answers:"
    print "-------------------"
    print " "

    missing_questions = list(set(db_tuple) - set(api_tuple))
         
    for ids in missing_questions:
        print "Updating question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("DELETE FROM so WHERE questionid = ?", (ids[0], ))
        conn.commit()
    
elif number_questions_db < number_questions_so_api:
    print "Adding Answers:"
    print "-----------------"
    print " "
       
    missing_questions = list(set(api_tuple) - set(db_tuple))
     
    for ids in missing_questions:
        print "Updating question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("INSERT INTO so (questionid,numberofanswers) VALUES (?,?)", (ids[0],ids[1]))           
        conn.commit() 
        



conn.close()


