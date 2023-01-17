from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

import shelve
                
class RegistrationForm(FlaskForm):
    username = StringField('Username : ',
                           render_kw={'placeholder' : 'Username'},
                           validators=[DataRequired(), Length(min = 2, max = 20)])
    firstName = StringField('First Name : ',
                            render_kw={'placeholder' : 'Benjamin'},
                            validators=[DataRequired(), Length(min = 2)])
    lastName = StringField('Last Name : ',
                           render_kw={'placeholder' : 'Franklin'},
                           validators=[DataRequired(), Length(min = 2)])
    email = StringField('Email : ',
                        render_kw={'placeholder' : 'BenjaminFranklin@example.com'},
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password : ',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password : ',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    
    def checkUserInDatabase(self, userEmail):
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        for keys in dictUsers:
            if self.email.data == str(dictUsers[keys].get_email()):
                raise ValidationError('User Already Created')

class LoginForm(FlaskForm):
    email = StringField('Email : ', #label
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password : ',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class EditForm(FlaskForm):
    editUsername = StringField('Username : ',
                        render_kw={'placeholder' : 'Username'},
                        validators=[DataRequired(), Length(min = 2, max = 20)])
    editFirstName = StringField('First Name : ',
                            render_kw={'placeholder' : 'Benjamin'},
                            validators=[DataRequired(), Length(min = 2)])
    editLastName = StringField('Last Name : ',
                           render_kw={'placeholder' : 'Franklin'},
                           validators=[DataRequired(), Length(min = 2)])
    editEmail = StringField('Email : ',
                        render_kw={'placeholder' : 'BenjaminFranklin@example.com'},
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Edit User')
