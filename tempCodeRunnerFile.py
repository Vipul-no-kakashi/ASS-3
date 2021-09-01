 error = "User Already Registered"
        print(users)
        return render_template('login.html', error=error)