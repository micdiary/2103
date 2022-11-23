from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
import os
from bson import json_util, ObjectId
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/2103_Assignment"
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


@app.route('/signup', methods=["GET", "POST"])
def sign_up():  # put application's code here
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        userExists = mongo.db.Account.find_one({'username': username}, {'username': 1, '_id': 0})
        # check if username exists
        if userExists:
            flash("existing username")
        else:
            mongo.db.Account.insert_one({'username': username, 'password': password})

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
            authUser = mongo.db.Account.find_one({'username': username, 'password': password},
                                                 {'username': 1, '_id': 0})
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
            eligibleCourses = db.find({'upper_bound': {'$gte': aggregate}},
                                      {'course_code': 1, 'course_name': 1, 'school_name': 1, 'polytechnic': 1,
                                       'lower_bound': 1, 'upper_bound': 1, '_id': 0}).sort(
                [('polytechnic', 1), ('upper_bound', 1)])


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
                    if i == schoolFilter[-1]:  # this part is just not adding the commas
                        school += i
                        break
                    school += i + ", "
                    filterQuery.append(i)

                eligibleCourses = db.find({'upper_bound': {'$gte': aggregate}, 'polytechnic': {"$in": filterQuery}},
                                          {'course_code': 1, 'course_name': 1, 'school_name': 1, 'polytechnic': 1,
                                           'lower_bound': 1, 'upper_bound': 1, '_id': 0}).sort(
                    [('polytechnic', 1), ('upper_bound', 1)])

            # get sql data
            # eligibleCourses = connectToDB(sqlQuery + " ORDER BY poly_name, upper_bound ASC")
            eligibleCourses = json_util.dumps(eligibleCourses)

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

            print('school ', school)
            print('poly', poly)
            schoolCourses = db.find({'school_name': school, 'polytechnic': poly}
                                    , {'course_code': 1, 'course_name': 1, 'polytechnic': 1, 'lower_bound': 1,
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


# upvote button submitted
@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    # check if user logged in
    login = validateLogin()

    if request.method == "POST":
        upvoted = request.form['upvote']

        # check if user has login and pressed upvote
        if upvoted and login:
            objectId = ObjectId(upvoted)
            checkVote = mongo.db.Comments.find({ '_id': objectId,'vote.username':login})
            voteExists = ""
            voteValue = ""

            # check if user voted before
            for i in checkVote:
                voteExists = i

            # if user voted bfe then update or remove vote value
            if voteExists:

                #find vote value
                getVoteValue = mongo.db.Comments.aggregate([
                    {
                        '$match': {
                            'vote':{
                                '$elemMatch':{
                                    '$and':[
                                        {'username': login},
                                        {'vote_value':1}
                                    ]
                                }
                            }, '_id': objectId
                        }
                    },
                    {
                        '$project':{

                            'vote':{
                                '$filter':{
                                    'input': '$vote',
                                    'as' : 'vote',
                                    'cond':{
                                        '$and':[
                                            {'$eq':[ '$$vote.username', login]},
                                            {'$eq': ['$$vote.vote_value',1]}
                                        ]
                                    }
                                }
                            }, '_id':0
                        }
                    }
                ])
                for i in getVoteValue:
                    voteValue =  i['vote'][0]['vote_value']
                # user upvoted bfe, so we remove
                if voteValue == 1:
                    mongo.db.Comments.update_one(
                        {
                            '_id':objectId
                        },
                        {
                            '$pull': {'vote':{'username':login,'vote_value':1}}
                         }

                    )
                    flash("upvote removed")
                # voteValue == -1, change to 1
                else:
                    mongo.db.Comments.update_one(
                        {
                            '_id': objectId,
                            'vote': {'username': login, 'vote_value': -1}
                        },
                        {
                            '$set': {'vote.$.vote_value': 1}
                        }
                    )
                    flash("upvote comment")

            # push new value into comment since it user never voted bfe
            else:
                mongo.db.Comments.update_one(
                    {
                        '_id': objectId
                    },
                    {
                        '$push': {'vote': {'username': login, 'vote_value': 1}}
                    }
                )
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
        downvoted = request.form['downvote']

        if downvoted and login:
            objectId = ObjectId(downvoted)
            checkVote = mongo.db.Comments.find({'_id': objectId, 'vote.username': login})
            voteExists = ""
            voteValue = ""

            # check if user voted before
            for i in checkVote:
                voteExists = i

            # if user voted bfe then update or remove vote value
            if voteExists:

                # find vote value
                getVoteValue = mongo.db.Comments.aggregate([
                    {
                        '$match': {
                            'vote': {
                                '$elemMatch': {
                                    '$and': [
                                        {'username': login},
                                        {'vote_value': -1}
                                    ]
                                }
                            }, '_id': objectId
                        }
                    },
                    {
                        '$project': {

                            'vote': {
                                '$filter': {
                                    'input': '$vote',
                                    'as': 'vote',
                                    'cond': {
                                        '$and': [
                                            {'$eq': ['$$vote.username', login]},
                                            {'$eq': ['$$vote.vote_value', -1]}
                                        ]
                                    }
                                }
                            }, '_id': 0
                        }
                    }
                ])
                for i in getVoteValue:
                    voteValue = i['vote'][0]['vote_value']
                # user downvoted bfe, so we remove
                if voteValue == -1:
                    mongo.db.Comments.update_one(
                        {
                            '_id': objectId
                        },
                        {
                            '$pull': {'vote': {'username': login, 'vote_value': -1}}
                        }

                    )
                    flash("downvote removed")
                # voteValue == 1, change to -1
                else:
                    mongo.db.Comments.update_one(
                        {
                            '_id': objectId,
                            'vote': {'username': login, 'vote_value': 1}
                        },
                        {
                            '$set': {'vote.$.vote_value': -1}
                        }
                    )
                    flash("downvote comment")

            # push new value into comment since it user never voted bfe
            else:
                mongo.db.Comments.update_one(
                    {
                        '_id': objectId
                    },
                    {
                        '$push': {'vote': {'username': login, 'vote_value': -1}}
                    }
                )
                flash("downvoted comment")

            return redirect(request.referrer)
        else:
            flash('Must be logged in to downvote')
            return redirect(request.referrer)


# comment  form submitted
@app.route('/eligible/comments', methods=['GET', 'POST'])
def comments():
    # check if user logged in
    login = validateLogin()

    # insert comments into db
    if request.method == "POST":
        comment = request.form['textbox']
        courseCode = request.form['course-code']

        # check if logged in
        if comment and login:
            # find user._id
            course = db.find_one({'course_code': courseCode}, {'_id': 1})
            user = mongo.db.Account.find_one({'username': login}, {'_id':1})
            # submit comment into course
            print(course)
            mongo.db.Comments.insert_one({'description': comment,
                                                    'course': course['_id'],
                                                    'commentor': user['_id'],
                                                    'vote':[
                                                    ]
                                                    })

            return redirect(request.url)
        else:
            flash('Must be logged in to comment')
            return redirect(request.url)

    # get course details
    course_code = request.args.get('comment')

    courseDetails = db.find({'course_code': course_code}
                            , {'course_code': 1, 'course_name': 1, 'school_name': 1, 'polytechnic': 1, 'lower_bound': 1,
                               'upper_bound': 1, '_id': 0})


    # retrieve comments section
    course = db.find_one({'course_code': course_code}, {'_id': 1})

    comments = mongo.db.Comments.aggregate([
        {'$match':
             {'course': course['_id']}
         },
        {'$lookup': {
            'from': "Account",
            'localField': "commentor",
            'foreignField': "_id",
            'as': "comments"}
        },
        {
            "$unwind": "$comments"
        },

        {'$project': {'description': 1, 'username': '$comments.username', '_id': 1,'votesum':{'$sum': '$vote.vote_value'}}}

    ])
    # highlight button if voted
    if login:
        highlightVote = mongo.db.Comments.find({'course': course['_id']},{'vote':1,'_id':0})
        value = []
        # if user voted then append vote value in value[]
        for i in highlightVote:
            # if empty means no votes, skip loop
            if i['vote'] == []:
                value.append(0)
                continue
            else:
                # check if user voted in comment, add vote value in [] if exists
                for x in i['vote']:

                    if login in x['username']:
                        tmp=x['vote_value']
                        break
                    else:
                        tmp= 0
                value.append(tmp)
        return render_template("comments.html", courseComments=comments, courseID=course_code,
                               chosenCourse=courseDetails, highlightVote = value,
                               login=login)

    return render_template("comments.html", courseComments=comments, courseID = course_code, chosenCourse = courseDetails,
                           login=login)


if __name__ == '__main__':
    app.run()
