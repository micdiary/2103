from flask import Flask, render_template, request, session, redirect, url_for, flash
import pymongo
from flask_pymongo import PyMongo
import os
from bson import json_util
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/2104_Assignment"
app.secret_key = os.urandom(24)
mongo = PyMongo(app)
db = mongo.db.School
###########################################################
# change to your own mySQL credentials and database names or it wont connect to your DB
###########################################################
host = 'localhost'
user = 'root'
passwd = 'root'
database = '2103_db'
app.debug = True


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
    if ('INSERT') in sqlCommand or ('DELETE') in sqlCommand:
        mydb.commit()

    DBData = json.dumps(mycursor.fetchall())
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
                return redirect(request.referrer)
            else:
                flash("wrong credentials")
                return redirect(request.referrer)
    return 'login success'


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
    # variableName = db.find({WHERE},{COLUMNS})
    # EXAMPLE:
    # online_users = db.find({'polytechnic': "RP"},{ 'course_name': 1, 'polytechnic': 1,  '_id': 0})

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
            eligibleCourses = db.find({'upper_bound': {'$gte':aggregate}},
                                      { 'course_code': 1,'course_name': 1,'school_name': 1, 'polytechnic': 1,
                                        'lower_bound': 1,'upper_bound': 1, '_id': 0}).sort( [('polytechnic',1),('upper_bound',1)])

            # sqlQuery = "SELECT course_code, course_name, school_name, poly_name, lower_bound, upper_bound " \
            #            "FROM course C, school S, polytechnic P " \
            #            "WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id" + " AND upper_bound >= " + str(
            #    aggregate)
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
            filterQuery = []
            if len(schoolFilter) > 0:
                school = ""
                for i in schoolFilter:
                    if i == schoolFilter[-1]: # this part is just not adding the commas
                        school += i
                        break
                    school += i+ ", "
                    filterQuery.append(i)

                eligibleCourses = db.find({'upper_bound': {'$gte':aggregate}, 'polytechnic': {"$in": filterQuery}},
                                      { 'course_code': 1,'course_name': 1,'school_name': 1, 'polytechnic': 1,
                                        'lower_bound': 1,'upper_bound': 1, '_id': 0}).sort( [('polytechnic',1),('upper_bound',1)])

            # get sql data
            #eligibleCourses = connectToDB(sqlQuery + " ORDER BY poly_name, upper_bound ASC")
            eligibleCourses= json_util.dumps(eligibleCourses)


            return redirect(
                url_for('eligible_courses', aggregate=aggregate, DBdata=eligibleCourses, school=school, login=login))

        # specific school courses form submitted
        if "school-course" in request.form:

            school = request.form["school"]
            polyNames = request.form["poly"].split()
            polyList = []
            poly = ""

            # string manipulation of poly name to get poly first letters (e.g. Singapore Poly = SP)
            for i in polyNames:
                poly += i[0]

            if poly == 'NP':
                poly = 'NYP'
            elif poly == 'NAP':
                poly = 'NP'

            print('school ',school)
            print('poly', poly)
            schoolCourses = db.find({'school_name': school, 'polytechnic': poly}
                                    ,{'course_code': 1, 'course_name': 1, 'polytechnic': 1,'lower_bound': 1,
                                      'upper_bound': 1, '_id': 0})

            schoolCourses = json_util.dumps(schoolCourses)

            return redirect(url_for('eligible_courses', DBdata=schoolCourses, schoolQuery=school, login=login))

        # scholarship for submitted
        if "school-scholarship" in request.form:
            school = request.form["school"]
            # get school scholarships and its descriptions as key value pairs
            scholarshipsOffered = db.find({'school_name': school}
                                    , {'scholarship': 1, '_id': 0}).distinct('scholarship')

            scholarshipsOffered = json_util.dumps(scholarshipsOffered)

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
        print(eligibleCourses)
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

    scholarshipsOffered = json.loads(request.args.get('DBdata'))

    return render_template('scholarships.html', scholarshipsOffered=scholarshipsOffered,
                           school=school, login=login)


# try to combine /upvote and /downvote with this
@app.route('/vote/<upOrDown>', methods=['GET', 'POST'])
def vote(upOrDown):
    print("test")
    return redirect(request.referrer)


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
                # delete downvote if exists
                deleteDownvote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d;" % (userID, upvoted)
                insertUpvote = "INSERT INTO vote ( user_id, comment_id, vote_value) VALUES (%d , %d , 1);" % (
                    userID, upvoted)
                connectToDB(deleteDownvote)
                connectToDB(insertUpvote)
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
                # delete downvote if exists
                deleteUpvote = "DELETE FROM vote WHERE user_id = %d AND comment_id = %d;" % (userID, downvoted)
                insertDownvote = "INSERT INTO vote ( user_id, comment_id, vote_value) VALUES (%d , %d , -1);" % (
                    userID, downvoted)
                connectToDB(deleteUpvote)
                connectToDB(insertDownvote)
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

            insertSQL = "INSERT INTO comments ( description, course_id, user_id) VALUES ('%s' , %d , %d);" % (
                comment, courseID[0][0], userID[0][0])
            connectToDB(insertSQL)

            return redirect(request.url)
        else:
            flash('Must be logged in to comment')
            return redirect(request.url)

    # retrieve comments section
    course_code = request.args.get('comment')

    # get sql of course
    courseSQLQuery = db.find({'course_code': course_code}
                            , {'course_code': 1, 'course_name': 1, 'school_name': 1,'polytechnic': 1, 'lower_bound': 1,
                               'upper_bound': 1, '_id': 0})
    # courseSQLQuery = "SELECT course_code, course_name,  school_name , poly_name, lower_bound, upper_bound" \
    #                  " FROM course C, school S, polytechnic P " \
    #                  " WHERE S.poly_id = P.poly_id AND S.school_id = C.school_id and course_code = " + course_code

    # get sql of comments
    courseSQLQuery = db.find({'course_code': course_code}
                             ,
                             {'course_code': 1, 'course_name': 1, 'school_name': 1, 'polytechnic': 1, 'lower_bound': 1,
                              'upper_bound': 1, '_id': 0})
    # commentsSQLQuery = "SELECT description, username, comment_id " \
    #                    "FROM comments C1, users U, course C2 " \
    #                    "WHERE U.user_id = C1.user_id " \
    #                    "AND C1.course_id = C2.course_id AND course_code = " + course_code + " " \
    #                                                                                         "ORDER BY comment_id ASC"
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
    return render_template("comments.html", courseComments=commentData, chosenCourse=courseData, votes=voteValues,
                           login=login)


if __name__ == '__main__':
    app.run()
