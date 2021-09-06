from flask import Flask, render_template, request
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
conn = mysql.connector.connect(
    host="ec2-35-153-114-74.compute-1.amazonaws.com",
    user="skvkwgmrcnwfzq",
    password="jsp1W5GGye",
    database='265384cd7737475bf58f1bba424e0bb78007e2fc674a77979137eba9c003d462',
    port="5432"
)
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('Signup.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    user_ID = request.form.get('user_Id')
    password = request.form.get('password')
    # password = generate_password_hash(password)
    cursor.execute("""SELECT * FROM users WHERE ID Like '{}'""".format(user_ID))
    users = cursor.fetchall()
    if len(users) > 0:
        if check_password_hash(users[0][2], password):
            return render_template("Success.html", user=user_ID)
        else:
            error = "Invalid Password"
            return render_template('login.html', error=error)
    else:
        error = "UserId is not Registered"
        return render_template('login.html', error=error)


@app.route('/forget_validation', methods=['POST'])
def forget_validation():
    user_Id = request.form.get('user_Id')
    Mno = request.form.get('Mno')
    cursor.execute("""SELECT * FROM users WHERE ID Like '{}' AND Mno Like '{}'""".format(user_Id, Mno))
    users = cursor.fetchall()
    if len(users) > 0:
        return render_template("reset.html", users_id=users[0][0])
    else:
        error = "User Id and Mobile no. not matched"
        return render_template('forget.html', error=error)


@app.route('/reset', methods=['POST'])
def reset():
    user_Id = request.form.get('user_Id')
    P1 = request.form.get('p1')
    P2 = request.form.get('p2')

    if (P1 != P2):
        error = "Password does not match"
        return render_template("reset.html", error=error)
    else:
        P1 = generate_password_hash(P1)
        cursor.execute("""UPDATE `users` SET `password` = '{}' WHERE (`ID` = '{}');""".format(P1, user_Id))
        conn.commit()
        success = "Password reset Successfully"
        return render_template("login.html", success=success)


@app.route('/forget')
def forget():
    return render_template('forget.html')


@app.route('/add_login', methods=['POST'])
def add_user():
    user_Id = request.form.get('Id')
    Mno = request.form.get('Mno')
    password = request.form.get('password')
    password = generate_password_hash(password)
    cursor.execute("""SELECT * FROM users WHERE ID Like '{}'""".format(user_Id))
    users = cursor.fetchall()
    if len(users) > 0:
        # return """SELECT * FROM users WHERE ID Like '{}'""".format(user_Id)
        error = "User Already Registered"
        print(users)
        return render_template('login.html', error=error)
    cursor.execute(
        """INSERT INTO users (`ID`, `Mno`, `password`) VALUES('{}', '{}', '{}');""".format(user_Id, Mno, password))
    conn.commit()
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port='8000')
