from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
###########################################################
# change to your own mySQL credentials and database names or it wont connect to your DB
###########################################################
host = 'localhost'
user = 'root'
passwd = 'root'
database = '2103_db'
app.debug = True

def connectToDB(sqlCommand):
    print(sqlCommand)
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    print("db connected")
    mycursor = mydb.cursor()
    # example command for sql queries
    mycursor.execute(sqlCommand)
    DBData = mycursor.fetchall()
    mycursor.close()
    return DBData
#main page
@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here
    # eligible courses form
    if request.method == "POST":
        aggregate = int(request.form["grade1"]) + int(request.form["grade2"]) + int(request.form["grade3"]) + int(
            request.form["grade4"]) + int(request.form["grade5"])
        eligibleCourses = connectToDB("SELECT course_code, course_name, school_name, poly_name, lower_bound, upper_bound FROM course C, school S, polytechnic P WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id AND upper_bound >= "+str(aggregate)+" AND lower_bound <= "+str(aggregate))

        return render_template("eligible.html", aggregate=aggregate , eligibleCourses = eligibleCourses)

    # example for retrieving data from db
    DBData = connectToDB("SELECT * FROM scholarship")
    return render_template("index.html", DBData = DBData)

#user can choose to login or not (must login if want to comment)
@app.route('/login')
def login():
    return 'login sucess'

#redirect from first form
@app.route('/eligible')
def eligible_courses():
    return 'courses eligible'

#redirect from second form
@app.route('/scholarships')
def scholarships_offered():
    return 'scholarships offered'


if __name__ == '__main__':
    app.run()
