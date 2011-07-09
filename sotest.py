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

questions_to_add = list(set(api_tuple) - set(db_tuple))
questions_to_delete = list(set(db_tuple) - set(api_tuple))
sorted_questions_to_add = sorted(questions_to_add)
sorted_questions_to_delete = sorted(questions_to_delete)

# Question Status!
print "Current Question Status:"
print "Total number of questions for %s on SO: %d" % (user.display_name, number_questions_so_api)    
print "Total number of questions for %s in DB: %d" % (user.display_name, number_questions_db)
print " "

# Check for new Questions
if number_questions_so_api == number_questions_db:
    print "No new questions!"
    print " "
elif number_questions_db < number_questions_so_api:
    print "Adding Questions:"
    print "-----------------"
    print " "
    for ids in questions_to_add:
        print "Inserting question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("INSERT INTO so (questionid,numberofanswers) VALUES (?,?)", (ids[0],ids[1]))           
        conn.commit()
elif number_questions_db > number_questions_so_api:
    print "Deleting Questions:"
    print "-------------------"
    print " "
    for ids in questions_to_delete:
        print "Deleting question ID: %d" % ids[0]
        print "Number of answers: %d" % ids[1]
        print " "
        c.execute("DELETE FROM so WHERE questionid = ?", (ids[0], ))
        conn.commit()    

# Update values if questions were added or removed
number_of_answers_db = [number_answers_db[0] for number_answers_db in c.execute('SELECT numberofanswers FROM so').fetchall()]
total_number_answers_db = sum(number_of_answers_db)
delete_list = []
for i in sorted_questions_to_delete:
    delete_list.append(i[0])
    delete_list.append(i[1])
add_list = []      
for i in sorted_questions_to_add:
    add_list.append(i[0])
    add_list.append(i[1])
both_lists = []
count = 0
for i in delete_list:
    both_lists.append(delete_list[count])
    both_lists.append(add_list[count])
    count += 1
final_list = zip(*[iter(both_lists)]*4)

      
# Answer Status!
print "Current Answer Status:"
print "Total number of answers for %s on SO: %d" % (user.display_name, total_number_answers_api)    
print "Total number of answers for %s in DB: %d" % (user.display_name, total_number_answers_db)
print " "

if total_number_answers_api == total_number_answers_db:
    print "No new answers!"
    print " "
elif total_number_answers_db != total_number_answers_api:
    print "Updating Answers:"
    print "---------------"
    print " "
    for values in final_list:
        print "Updating answer count in id %d from %d to %d" % (values[0], values[2], values[3]) 
        c.execute("UPDATE so SET numberofanswers=? WHERE questionid=?", (values[3],values[0]))
        conn.commit()
        
conn.close()
