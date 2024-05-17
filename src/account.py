from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Email, DataRequired

#user session
class AuthUser:
    def __init__(
       self,
       username     
    ):
        self.username = username

    def __repr__(self) -> str:
        return (f"AuthUser(username='{self.username}')")
    
    def to_dict(self):
        return {
            'username': self.username
        }


class UserProfile:
    def __init__(
       self,
       username,
       email,
       password     
    ):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return (f"AuthUser(username='{self.username}',"
                f"email='{self.email}',"
                f"password='{self.password}')")
    
    def to_dict(self):
        return {
            'username': self.username,
            'email':self.email,
            'password':self.password
        }

class SignUpForm(FlaskForm):
    username=StringField('username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired()])
    password=PasswordField('password', validators=[DataRequired()])

def signUpUser(UserProfile): 
    print (UserProfile.password)    
