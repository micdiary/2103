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

    mycursor.execute(sqlCommand)
    DBData = mycursor.fetchall()
    mycursor.close()
    return DBData
#main page
@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here

    if request.method == "POST":
        # eligible courses form
        if "eligible-course" in request.form:
            # get total aggregate
            school = "all polytechnics"
            aggregate = int(request.form["grade1"]) + int(request.form["grade2"]) + int(request.form["grade3"]) + int(
                request.form["grade4"]) + int(request.form["grade5"])
            sqlQuery = "SELECT course_code, course_name, school_name, poly_name, lower_bound, upper_bound " \
                       "FROM course C, school S, polytechnic P " \
                       "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id" + " AND upper_bound >= " + str(aggregate)
            # get filter conditions
            schoolFilter = []
            if request.form.get('NYP') == 'NYP':
                schoolFilter.append("NYP")
            if request.form.get('NP') == 'NP':
                schoolFilter.append("NP")
            if request.form.get('SP') == 'SP':
                schoolFilter.append("SP")
            if request.form.get('TP') == 'TP':
                schoolFilter.append("TP")
            if request.form.get('RP') == 'RP':
                schoolFilter.append("RP")

            filterQuery = "("
            if len(schoolFilter) > 0:
                school = ""
                for i in schoolFilter:
                    if i != schoolFilter[-1]:
                        filterQuery += "'"+i+"',"
                        school += i + ", "
                    else:
                        filterQuery += "'"+i+"')"
                        school += i
                sqlQuery += " AND poly_name IN "+filterQuery

            # get sql data
            eligibleCourses = connectToDB(sqlQuery+" ORDER BY poly_name, upper_bound ASC")

            return render_template("eligible.html", aggregate=aggregate , eligibleCourses = eligibleCourses, school = school)

        # specific poly courses form
        if "poly-course" in request.form:

            polytechnic = "'"+request.form["poly-names"]+"'"
            sqlQuery = "SELECT course_code, course_name, school_name, poly_name, lower_bound, upper_bound " \
                       "FROM course C, school S, polytechnic P " \
                       "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id AND poly_name = "+ polytechnic
            DBdata = connectToDB(sqlQuery)
            return render_template("eligible.html", eligibleCourses = DBdata)

    return render_template("index.html")

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
