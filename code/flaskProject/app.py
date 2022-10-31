from flask import Flask, render_template, request, session, g, redirect, url_for
import mysql.connector
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)
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
    DBData = json.dumps(mycursor.fetchall())
    mycursor.close()
    return DBData


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


# main page
@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here

    if request.method == "POST":
        # eligible courses form
        if "login-attempt" in request.form:
            username = request.form['username']
            password = request.form['password']
            sqlQuery = "SELECT 1 from users WHERE username = " + "'" + username + "'" + " AND password = " + "'" + password + "'"
            authUser = connectToDB(sqlQuery)
            print(authUser)
            session.pop('user', None)
            if authUser:
                session['user'] = username
                return render_template("index.html", login=username)
            return render_template("index.html")

        if "eligible-course" in request.form:
            # get total aggregate
            school = "all polytechnics"
            aggregate = int(request.form["grade1"]) + int(request.form["grade2"]) + int(request.form["grade3"]) + int(
                request.form["grade4"]) + int(request.form["grade5"])
            sqlQuery = "SELECT course_code, course_name, school_name, poly_name, lower_bound, upper_bound " \
                       "FROM course C, school S, polytechnic P " \
                       "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id" + " AND upper_bound >= " + str(
                aggregate)
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
                        filterQuery += "'" + i + "',"
                        school += i + ", "
                    else:
                        filterQuery += "'" + i + "')"
                        school += i
                sqlQuery += " AND poly_name IN " + filterQuery

            # get sql data
            eligibleCourses = connectToDB(sqlQuery + " ORDER BY poly_name, upper_bound ASC")

            return redirect(url_for('eligible_courses',  aggregate=aggregate, DBdata=eligibleCourses, school=school))
            #return render_template("eligible.html", aggregate=aggregate, eligibleCourses=eligibleCourses, school=school)


        # specific school courses form
        if "school-course" in request.form:

            polyNames = request.form["poly"].split()
            poly = ""
            for i in polyNames:
                poly += i[0]
            print(poly)
            if poly == 'NP':
                poly = 'NYP'
            elif poly == 'NAP':
                poly = 'NP'

            school = request.form["school"]
            sqlQuery = ("SELECT course_code, course_name, poly_name, lower_bound, upper_bound " \
                      "FROM course C, school S, polytechnic P " \
                      "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id AND poly_name = '%s' AND school_name = '%s'"%(poly,school))
            print(sqlQuery)
            DBdata = connectToDB(sqlQuery)

            return redirect(url_for('eligible_courses', DBdata=DBdata, schoolQuery = True))
            #return render_template("eligible.html", schoolQuery=True, eligibleCourses=DBdata)
    return render_template("index.html")


# user can choose to login or not (must login if want to comment)
@app.route('/login')
def login():

    return 'login sucess'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# redirect from first form
@app.route('/eligible')
def eligible_courses():
    try:
        if session['user']:
            login = session['user']
    except:
        login = False


    eligibleCourses = json.loads(request.args.get('DBdata'))
    schoolQuery = request.args.get('schoolQuery')
    school = request.args.get('aggregate')
    aggregate = request.args.get('school')
    if schoolQuery:
        return render_template("eligible.html", schoolQuery = schoolQuery , eligibleCourses = eligibleCourses, login = login )
    elif school:
        return render_template("eligible.html", aggregate=aggregate, eligibleCourses=eligibleCourses, school=school, login = login)


    return render_template("eligible.html")

# redirect from second form
@app.route('/scholarships')
def scholarships_offered():
    return 'scholarships offered'

@app.route('/eligible/comments', methods=['GET', 'POST'])
def comments():
    course_code = "'"+request.args.get('comment')+"'"
    print(course_code)
    sqlQuery = "SELECT description, username" \
               " FROM comments C2, course C1, users" \
               " WHERE C1.course_id = C2.course_id and C1.course_code = "+ course_code
    DBdata = json.loads(connectToDB(sqlQuery))
    return render_template("comments.html", courseComments = DBdata)

if __name__ == '__main__':
    app.run()
