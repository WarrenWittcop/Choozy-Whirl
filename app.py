# base packages
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os

# custom things I wrote
from src.account import SignUpForm, signUpUser, UserProfile

# must do at the top of any file where accessing env variable
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


# route for home
@app.route('/')
def hello():
    return render_template('home.html')

# route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signupuserroute():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        userprofile = UserProfile(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        user_collection = mongo.db.users
        if user_collection.find_one({'username': userprofile.username}):
            return render_template('signup.html', form=form, error="Username already exists")
        
        signUpUser(mongo, userprofile) 
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

# route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        user_collection = mongo.db.users
        user = user_collection.find_one({'$or': [{'username': identifier}, {'email': identifier}]})

        if user and user['password'] == password:
            session['user_id'] = user['username']
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

# route for profile
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    username = session['user_id']
    user_collection = mongo.db.users
    user = user_collection.find_one({'username': username})
    user_wheels = user.get('wheels', [])

    return render_template('profile.html', username=username, user_wheels=user_wheels)

# route for wheels
@app.route('/wheels', methods=['GET', 'POST'])
def wheels():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_collection = mongo.db.users
    user = user_collection.find_one({'username': user_id})

    user_wheels = user.get('wheels', [])

    if request.method == 'POST':
        action = request.form['action']
        if action == 'create':
            wheel_name = request.form['wheel_name']
            options = [option.strip() for option in request.form['options'].split(',')]
            user_wheels.append({'name': wheel_name, 'options': options})
        elif action == 'delete':
            wheel_index = int(request.form['wheel_index'])
            del user_wheels[wheel_index]
        elif action == 'update':
            wheel_index = int(request.form['wheel_index'])
            wheel_name = request.form['wheel_name']
            options = [option.strip() for option in request.form.getlist('options[]') if option.strip()]
            user_wheels[wheel_index] = {'name': wheel_name, 'options': options}

        user_collection.update_one({'username': user_id}, {'$set': {'wheels': user_wheels}})

        return redirect(url_for('wheels'))

    return render_template('wheels.html', user_wheels=user_wheels)

@app.route('/get-wheel-options', methods=['GET'])
def get_wheel_options():
    if 'user_id' not in session:
        return jsonify(options=[]), 403

    wheel_name = request.args.get('wheel_name')
    user_id = session['user_id']
    user_collection = mongo.db.users
    user = user_collection.find_one({'username': user_id})
    user_wheels = user.get('wheels', [])
    wheel = next((wheel for wheel in user_wheels if wheel['name'] == wheel_name), None)

    if wheel:
        return jsonify(options=wheel['options'])
    else:
        return jsonify(options=[]), 404
    
# route for editing a wheel
@app.route('/edit_wheel/<int:wheel_index>', methods=['GET', 'POST'])
def edit_wheel(wheel_index):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_collection = mongo.db.users
    user = user_collection.find_one({'username': user_id})

    user_wheels = user.get('wheels', [])
    wheel = user_wheels[wheel_index]

    if request.method == 'POST':
        # Update the wheel details
        wheel_name = request.form['wheel_name']
        options = [option.strip() for option in request.form.getlist('options[]') if option.strip()]
        user_wheels[wheel_index] = {'name': wheel_name, 'options': options}
        user_collection.update_one({'username': user_id}, {'$set': {'wheels': user_wheels}})

        return redirect(url_for('wheels'))

    return render_template('wheeledit.html', wheel=wheel, wheel_index=wheel_index)    

@app.route('/delete_wheel/<int:wheel_index>', methods=['POST'])
def delete_wheel(wheel_index):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_wheels = session.get('user_wheels', [])
    if 0 <= wheel_index < len(user_wheels):
        del user_wheels[wheel_index]
        session['user_wheels'] = user_wheels

    return redirect(url_for('wheels'))

# route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('hello'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=port, host='0.0.0.0')