from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Email, DataRequired

class AuthUser:
    def __init__(self, username):
        self.username = username

    def __repr__(self) -> str:
        return f"AuthUser(username='{self.username}')"
    
    def to_dict(self):
        return {
            'username': self.username
        }

class UserProfile:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return (f"UserProfile(username='{self.username}',"
                f"email='{self.email}',"
                f"password='{self.password}')")
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

def signUpUser(mongo, user_profile):
    user_collection = mongo.db.users
    user_collection.insert_one(user_profile.to_dict())
