#base packages
from flask import Flask,render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

#custom things I wrote
from src.account import SignUpForm, signUpUser, UserProfile

#must do at the top of any file where accessing env variable
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#test data for user login
users = {
    'user1': {'email': 'user1@example.com', 'password': 'password1'},
    'user2': {'email': 'user2@example.com', 'password': 'password2'}
}

#route for home
@app.route('/')
def hello():
    return render_template('home.html')

#route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signupuserroute():
    form=SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        userprofile=UserProfile(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        signUpUser(userprofile)
        users[userprofile.username] = {'email': userprofile.email, 'password': userprofile.password}
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

#route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        
        # Check if the identifier is a username or email
        user = None
        for username, details in users.items():
            if identifier == username or identifier == details['email']:
                user = {'username': username, 'password': details['password']}
                break
        
        # Validate password
        if user and user['password'] == password:
            session['user_id'] = user['username']
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

# Route for profile
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    username = session['user_id']
    return render_template('profile.html', username=username)

@app.route('/wheels')
def wheels():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    #function get_user_wheels()
    user_wheels = get_user_wheels(user_id) 

    return render_template('wheels.html', user_wheels=user_wheels)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)