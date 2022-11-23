from flask import Flask, render_template, request, session, redirect, url_for, flash
from decimal import *
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


# to jsonify decimals values for vote
# https://bobbyhadz.com/blog/python-typeerror-object-of-type-decimal-is-not-json-serializable#:~:text=The%20Python%20%22TypeError%3A%20Object%20of,string%20to%20preserve%20its%20precision.
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


# pull or push data from/to mySQL
def connectToDB(sqlCommand):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    print("db connected")
    mycursor = mydb.cursor()
    print("sql command: " + sqlCommand)
    mycursor.execute(sqlCommand)
    if ('INSERT') in sqlCommand or ('DELETE') in sqlCommand or ('UPDATE') in sqlCommand:
        mydb.commit()

    DBData = json.dumps(mycursor.fetchall(), cls=DecimalEncoder)
    mycursor.close()
    return DBData


@app.route('/signup', methods=["GET", "POST"])
def sign_up():  # put application's code here
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sqlQuery = "SELECT 1 from users WHERE username = " + "'" + username + "'"
        userExists = json.loads(connectToDB(sqlQuery))
        # check if username exists
        if userExists:
            flash("existing username")
        else:
            insertSQL = "INSERT INTO users ( username, password) VALUES ('%s' , '%s' );" % (username, password)
            connectToDB(insertSQL)
            session['user'] = username
            return redirect(url_for('index'))
    return render_template("signup.html")


# login is optional (must login if want to comment/vote)
@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        # eligible courses form
        if "login-attempt" in request.form:
            username = request.form['username']
            password = request.form['password']
            sqlQuery = "SELECT 1 from users WHERE username = " + "'" + username + "'" + " AND password = " + "'" + password + "'"
            authUser = json.loads(connectToDB(sqlQuery))
            session.pop('user', None)
            if authUser:
                session['user'] = username
                return redirect(url_for('index'))
            else:
                flash("wrong credentials")
                return redirect(request.referrer)
    return 'login success'

@app.route('/login-form')
def loginForm():
    session.pop('user', None)
    return render_template("login-form.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


def validateLogin():
    try:
        if session['user']:
            login = session['user']
    except:
        login = False

    return login


# main page
@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here
    login = validateLogin()
    if request.method == "POST":
        if "sign-up" in request.form:
            return redirect(url_for('sign_up'))
        # eligible-courses form submitted
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

            # string manipulation of poly name for sql query
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

            return redirect(
                url_for('eligible_courses', aggregate=aggregate, DBdata=eligibleCourses, school=school, login=login))
            # return render_template("eligible.html", aggregate=aggregate, eligibleCourses=eligibleCourses, school=school)

        # specific school courses form submitted
        if "school-course" in request.form:

            school = request.form["school"]
            polyNames = request.form["poly"].split()
            poly = ""

            # string manipulation of poly name for sql query
            for i in polyNames:
                poly += i[0]

            if poly == 'NP':
                poly = 'NYP'
            elif poly == 'NAP':
                poly = 'NP'

            sqlQuery = ("SELECT course_code, course_name, poly_name, lower_bound, upper_bound " \
                        "FROM course C, school S, polytechnic P " \
                        "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id AND poly_name = '%s' AND school_name = '%s'" % (
                            poly, school))

            DBdata = connectToDB(sqlQuery)

            return redirect(url_for('eligible_courses', DBdata=DBdata, schoolQuery=True, login=login))

        # scholarship for submitted
        if "school-scholarship" in request.form:
            school = request.form["school"]
            # get school id
            schoolIDSQL = " SELECT school_id FROM school WHERE school_name ='%s'" % (school)
            schoolID = json.loads(connectToDB(schoolIDSQL))

            scholarshipOfferedSQL = "SELECT scholarship_name " \
                                    "FROM school SL, school_scholarship SSP, scholarship SP " \
                                    "WHERE SL.school_id = SSP.school_id " \
                                    "AND SP.scholarship_id = SSP.scholarship_id AND SL.school_id = %d" % (
                                        int(schoolID[0][0]))

            scholarshipsOffered = connectToDB(scholarshipOfferedSQL)

            return redirect(url_for('scholarships_offered', DBdata=scholarshipsOffered, school=school, login=login))

    return render_template("index.html", login=login)


# redirect from eligible-courses form
@app.route('/eligible')
def eligible_courses():
    # check if user logged in
    login = validateLogin()

    eligibleCourses = json.loads(request.args.get('DBdata'))
    schoolQuery = request.args.get('schoolQuery')
    school = request.args.get('aggregate')
    aggregate = request.args.get('school')
    if schoolQuery:
        return render_template("eligible.html", schoolQuery=schoolQuery, eligibleCourses=eligibleCourses, login=login)
    elif school:
        return render_template("eligible.html", aggregate=aggregate, eligibleCourses=eligibleCourses, school=school,
                               login=login)

    return render_template("eligible.html")


# redirect from school-scholarship form
@app.route('/scholarships')
def scholarships_offered():
    # check if user logged in
    login = validateLogin()
    school = request.args.get('school')

    criteriaList = []
    scholarshipsOffered = json.loads(request.args.get('DBdata'))

    # get all scholarship criteria from database
    for i in scholarshipsOffered:
        getCriteriaSQL = "SELECT criteria_description FROM school SL, school_scholarship SSP, scholarship SP, scholarship_criteria SPC, criteria C " \
                         "WHERE SL.school_id = SSP.school_id " \
                         "AND SP.scholarship_id = SSP.scholarship_id " \
                         "AND SP.scholarship_id = SPC.scholarship_id " \
                         "AND SPC.criteria_id = C.criteria_id " \
                         "AND scholarship_name = \"%s\" AND school_name = '%s'" % (i[0], school)
        criteriaData = json.loads(connectToDB(getCriteriaSQL))

        criteriaList.append(criteriaData)

    return render_template('scholarships.html', scholarshipsOffered=scholarshipsOffered, criteriaList=criteriaList,
                           school=school, login=login)



# upvote button submitted
@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    # check if user logged in
    login = validateLogin()
    print("test")
    if request.method == "POST":
        upvoted = int(request.form['upvote'])
        # check if user has login and pressed upvote
        if upvoted and login:
            userID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))
            userID = int(userID[0][0])
            # check if user voted before
            upvotedBefore = json.loads(connectToDB(
                "SELECT 1 FROM vote WHERE comment_id = %d AND user_id = %d AND vote_value = 1" % (upvoted, userID)))
            # check if user has upvoted before
            if upvotedBefore:
                # undo the upvote
                undoUpVote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d AND vote_value = 1 ;" % (
                    userID, upvoted)
                flash("upvote removed")
                connectToDB(undoUpVote)
            else:
                # update if vote exists
                updateUpvote = "UPDATE vote SET vote_value = 1 WHERE user_id = %d AND comment_id = %d;" % (userID, upvoted)


                connectToDB(updateUpvote)
                flash("upvoted comment")

            return redirect(request.referrer)
        else:
            flash('Must be logged in to upvote')
            return redirect(request.referrer)

    return redirect(request.referrer)


@app.route('/downvote', methods=['GET', 'POST'])
def downvote():
    # check if user logged in
    login = validateLogin()
    if request.method == "POST":
        downvoted = int(request.form['downvote'])

        if downvoted and login:
            userID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))
            userID = int(userID[0][0])
            # check if user voted before
            downvotedBefore = json.loads(connectToDB(
                "SELECT 1 FROM vote WHERE comment_id = %d AND user_id = %d AND vote_value = -1" % (downvoted, userID)))
            if downvotedBefore:
                # undo the upvote
                undoDownVote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d AND vote_value = -1;" % (
                    userID, downvoted)
                connectToDB(undoDownVote)
                flash("downvote removed")
            else:
                # update downvote if exists
                updateUpvote = "UPDATE vote SET vote_value = -1 WHERE user_id = %d AND comment_id = %d;" % (
                userID, downvoted)

                connectToDB(updateUpvote)
                flash("downvoted comment")
            return redirect(request.referrer)
        else:
            flash('Must be logged in to downvote')
            return redirect(request.referrer)

    return redirect(request.referrer)


# comment  form submitted
@app.route('/eligible/comments', methods=['GET', 'POST'])
def comments():
    # check if user logged in
    login = validateLogin()

    # insert comments into db
    if request.method == "POST":
        comment = request.form['textbox']
        courseNo = request.form['course-code']

        # check if logged in
        if comment and login:
            # submit comment into course
            courseID = json.loads(connectToDB("SELECT course_id FROM course WHERE course_code = '%s'" % (courseNo)))
            userID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))

            insertSQL = "INSERT INTO comments ( description, course_id, user_id) VALUES ('%s' , %d , %d);" % (comment, courseID[0][0], userID[0][0])
            connectToDB(insertSQL)

            return redirect(request.url)
        else:
            flash('Must be logged in to comment')
            return redirect(request.url)

    # retrieve comments section
    course_code = "'" + request.args.get('comment') + "'"

    # get sql of course
    courseSQLQuery = "SELECT course_code, course_name,  school_name , poly_name, lower_bound, upper_bound" \
                     " FROM course C, school S, polytechnic P " \
                     " WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id and course_code = " + course_code

    # get sql of comments
    commentsSQLQuery = "SELECT description, username, comment_id " \
                       "FROM comments C1, users U, course C2 " \
                       "WHERE U.user_id = C1.user_id " \
                       "AND C1.course_id = C2.course_id AND course_code = " + course_code + " " \
                                                                                            "ORDER BY comment_id ASC"
    # get vote of comments
    voteSQLQuery = "SELECT C1.comment_id, SUM(vote_value) " \
                   "FROM  vote V, comments C1, users U, course C2 " \
                   "WHERE V.comment_id = C1.comment_id " \
                   "AND U.user_id = C1.user_id " \
                   "AND C1.course_id = C2.course_id " \
                   "AND course_code = " + course_code + " " \
                                                        "GROUP BY V.comment_id " \
                                                        "ORDER BY comment_id ASC"
    commentData = json.loads(connectToDB(commentsSQLQuery))
    courseData = json.loads(connectToDB(courseSQLQuery))
    voteValues = json.loads(connectToDB(voteSQLQuery))

    # only highlight upvotes if user logged in
    if login:
        getCourseID = json.loads(connectToDB("SELECT course_id FROM course WHERE course_code = %s"%(course_code)))

        getUserID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))

        gethighLightVote = "SELECT description, V.vote_value " \
                        "FROM vote V, comments C1, users U, course C2 " \
                        "WHERE V.comment_id = C1.comment_id " \
                        "AND C1.course_id = %d AND V.user_id = %d " \
                                                 "GROUP BY V.comment_id"%(getCourseID[0][0],getUserID[0][0])

        highLightVote = json.loads(connectToDB(gethighLightVote))

        print(highLightVote)
        return render_template("comments.html", courseComments=commentData, chosenCourse=courseData, votes=voteValues,
                               hightLightVote = highLightVote, login=login)

    return render_template("comments.html", courseComments=commentData, chosenCourse=courseData, votes=voteValues,
                           login=login)


if __name__ == '__main__':
    app.run()
