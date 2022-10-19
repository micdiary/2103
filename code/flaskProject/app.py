from flask import Flask, render_template
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

#main page
@app.route('/')
def index():  # put application's code here
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    print("db connected")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM scholarship")
    DBData = mycursor.fetchall()
    mycursor.close()

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
