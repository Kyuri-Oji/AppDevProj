from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from eventForms import eventCreateForm
import shelve


from OOP.eventFunction import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ecce6a32ba6703d10b72f3ccea07175'

# Main pages
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/contact')
@app.route('/about')
def contact():
    return render_template('forms.html')

@app.route('/overview')
def overview():
    return render_template('overview.html', title = 'Overview')

# User Functions
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        
        dictUsers = {}
        db = shelve.open('users', 'c')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')

        flash(f'Account created for {form.username.data}!', '')
        return redirect(url_for('home'))
    return render_template('registration.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', '')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title = 'Login', form=form)

@app.route('/users')
def users():
    form = LoginForm()
    return render_template('users.html')
    
# Event Functions
@app.route('/events/createEvents', methods=['GET', 'POST'])
def createEvents():
    formEvents = eventCreateForm()
    if formEvents.validate_on_submit() and request.method == 'POST':
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
        eventName = formEvents.eventName.data
        eventDesc = formEvents.eventDesc.data
        eventVacancy = formEvents.eventVacancy.data
        eventDate = formEvents.eventDate.data
        
        createEvents(eventName, eventDesc, eventVacancy, eventDate)
        eventsDict[createEvents.eventCount] = createEvents
        eventDB['Events'] = eventsDict
        
        eventDB.close()
        
        return redirect(url_for('home'))
    return render_template('Events/eventCreate.html', formEvents=formEvents)    

@app.route('/events')
def eventsPage():
    return render_template('Events/eventMain.html')

if __name__ == '__main__':
    app.run(debug=True)