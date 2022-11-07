from flask import Flask, render_template, request, session, g, redirect, url_for, flash
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

def connectToDB(sqlCommand):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    print("db connected")
    mycursor = mydb.cursor()

    mycursor.execute(sqlCommand)
    if ('INSERT') in sqlCommand or ('DELETE') in sqlCommand:
        print("sql command: " + sqlCommand)
        mydb.commit()
    DBData = json.dumps(mycursor.fetchall(), cls=DecimalEncoder)
    mycursor.close()
    return DBData


def validateLogin():
    try:
        if session['user']:
            login = session['user']
    except:
        login = False

    return login


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


# main page
@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here
    login = validateLogin()
    if request.method == "POST":
        if "sign-up" in request.form:
            return redirect(url_for('sign_up'))

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

            return redirect(
                url_for('eligible_courses', aggregate=aggregate, DBdata=eligibleCourses, school=school, login=login))
            # return render_template("eligible.html", aggregate=aggregate, eligibleCourses=eligibleCourses, school=school)

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
                        "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id AND poly_name = '%s' AND school_name = '%s'" % (
                        poly, school))
            print(sqlQuery)
            DBdata = connectToDB(sqlQuery)

            return redirect(url_for('eligible_courses', DBdata=DBdata, schoolQuery=True, login=login))
            # return render_template("eligible.html", schoolQuery=True, eligibleCourses=DBdata)

    return render_template("index.html", login=login)


@app.route('/signup', methods=["GET", "POST"])
def sign_up():  # put application's code here
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sqlQuery = "SELECT 1 from users WHERE username = " + "'" + username + "'"
        userExists = json.loads(connectToDB(sqlQuery))

        if userExists:
            flash("existing username")
        else:
            insertSQL = "INSERT INTO users ( username, password) VALUES ('%s' , '%s' );" % (username, password)
            connectToDB(insertSQL)
            session['user'] = username
            return redirect(url_for('index'))
    return render_template("signup.html")


# user can choose to login or not (must login if want to comment)
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
                return redirect(request.referrer)
            else:
                flash("wrong credentials")
                return redirect(request.referrer)
    return 'login sucess'


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# redirect from first form
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


# redirect from second form
@app.route('/scholarships')
def scholarships_offered():
    return 'scholarships offered'


# try to combine /upvote and /downvote with this
@app.route('/vote/<upOrDown>', methods=['GET', 'POST'])
def vote(upOrDown):
    print("test")
    return redirect(request.referrer)


@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    # check if user logged in
    login = validateLogin()
    print("test")
    if request.method == "POST":
        upvoted = int(request.form['upvote'])

        if upvoted and login:
            userID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))
            userID = int(userID[0][0])
            # check if user voted before
            upvotedBefore = json.loads(connectToDB(
                "SELECT 1 FROM vote WHERE comment_id = %d AND user_id = %d AND vote_value = 1" % (upvoted, userID)))

            if upvotedBefore:

                undoUpVote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d AND vote_value = 1 ;" % (userID, upvoted)
                connectToDB(undoUpVote)
            # else upvote
            else:
                # delete downvote if exists
                deleteDownvote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d;" % (userID, upvoted)
                insertUpvote = "INSERT INTO vote ( user_id, comment_id, vote_value) VALUES (%d , %d , 1);" % (
                userID, upvoted)
                connectToDB(deleteDownvote)
                connectToDB(insertUpvote)

            flash("vote registered")
            return redirect(request.referrer)
        else:
            flash('Must be logged in to upvote')
            return redirect(request.referrer)

    return redirect(request.referrer)


@app.route('/downvote', methods=['GET', 'POST'])
def downvote():
    # check if user logged in
    print("test2")
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
                undoDownVote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d AND vote_value = -1;" % (userID, downvoted)
                connectToDB(undoDownVote)
            # else upvote
            else:
                # delete downvote if exists
                deleteUpvote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d;" % (userID, downvoted)
                insertDownvote = "INSERT INTO vote ( user_id, comment_id, vote_value) VALUES (%d , %d , -1);" % (
                userID, downvoted)
                connectToDB(deleteUpvote)
                connectToDB(insertDownvote)
            flash("vote registered")
            return redirect(request.referrer)
        else:
            flash('Must be logged in to downvote')
            return redirect(request.referrer)

    return redirect(request.referrer)


@app.route('/eligible/comments', methods=['GET', 'POST'])
def comments():
    # check if user logged in
    login = validateLogin()

    # insert comments into db
    if request.method == "POST":
        print("getting comment and courseNumber")
        comment = request.form['textbox']
        courseNo = request.form['course-code']
        print("comment: " + comment)
        print("courseNo: " + courseNo)
        # check if logged in
        if comment and login:
            courseID = json.loads(connectToDB("SELECT course_id FROM course WHERE course_code = '%s'" % (courseNo)))
            userID = json.loads(connectToDB("SELECT user_id FROM users WHERE username = '%s'" % (login)))
            print(courseID[0][0])
            print(userID[0][0])
            insertSQL = "INSERT INTO comments ( description, course_id, user_id) VALUES ('%s' , %d , %d);" % (
            comment, courseID[0][0], userID[0][0])
            print("insertSQl: " + insertSQL)
            connectToDB(insertSQL)

            return redirect(request.url)
        else:
            flash('Must be logged in to comment')
            print("login fail")
            return redirect(request.url)

    # retrieve comments section
    course_code = "'" + request.args.get('comment') + "'"
    print(course_code)
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
    print(courseData)
    # my_url = url_for('search_bp.search', book=book, author=author)
    return render_template("comments.html", courseComments=commentData, chosenCourse=courseData, votes = voteValues, login=login)

if __name__ == '__main__':
    app.run()
