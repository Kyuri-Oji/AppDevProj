from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError

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
    phoneNo = IntegerField('Phone Number : ',
                           render_kw={'placeholder' : '98765432'},
                           validators=[DataRequired(), NumberRange(min=80000000, max=99999999)])
    password = PasswordField('Password : ',
                             validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField('Confirm Password : ',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    
    def validate_email(self, userEmail):
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        for keys in dictUsers:
            if self.email.data == str(dictUsers[keys].get_email()):
                raise ValidationError('Email already registered.')
            
    def validate_phoneNo(self, userPhoneNo):
        dictUsers = {}
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        for keys in dictUsers:
            if self.phoneNo.data == (dictUsers[keys].get_phoneNo()):
                raise ValidationError('Phone Number already registered.')


class LoginForm(FlaskForm):
    loginField = StringField('Email or Phone Number : ', #label
                        validators=[DataRequired()])
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
    editPhoneNo = IntegerField('Phone Number : ',
                               render_kw={'placeholder' : '98765432'},
                               validators=[DataRequired()])

    submit = SubmitField('Update')

class userSearchForm(FlaskForm):
    userSearchItem = StringField('Search : ',
                                  validators=[DataRequired(message='Search input cannot be empty')])
    submit = SubmitField('Search')