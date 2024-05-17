#base packages
from flask import Flask,render_template, request, redirect, url_for
from dotenv import load_dotenv
import os

#custom things I wrote
from src.account import SignUpForm, signUpUser, UserProfile

#must do at the top of any file where accessing env variable
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        return redirect(url_for('hello'))
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=5000)