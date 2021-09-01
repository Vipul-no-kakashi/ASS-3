from flask import Flask, render_template, request, flash
import mysql.connector
app = Flask(__name__)
conn = mysql.connector.connect(
  host="remotemysql.com",
  user="RJK7rOrATq",
  password="zsgyihfQls",
  database='RJK7rOrATq'
)
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return render_template('login.html')
    # return 'Hello World!'


@app.route('/signup')
def signup():
    return render_template('Signup.html')

@app.route('/login_validation', methods = ['POST'])
def login_validation():
    user_ID = request.form.get('user_Id')
    passowrd = request.form.get('password')
    cursor.execute("""SELECT * FROM users WHERE ID Like '{}' AND password Like '{}'""".format(user_ID, passowrd))
    users = cursor.fetchall()
    if len(users)>0:
        return render_template("Success.html")
    else:
        error = "Invalid password or UserId"
        return render_template('login.html', error=error)

@app.route('/add_login', methods = ['POST'])
def add_user():
    user_Id = request.form.get('Id')
    Mno = request.form.get('Mno')
    password = request.form.get('password')
    cursor.execute("""INSERT INTO users (`ID`, `Mno`, `password`) VALUES('{}', '{}', '{}');""".format(user_Id, Mno, password))
    conn.commit()
    # return render_template('login.html')
    return "Login ADDed"
if __name__ == '__main__':
    app.run(debug=True, port='8000')
