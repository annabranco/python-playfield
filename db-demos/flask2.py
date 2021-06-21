# Running the flask app
# To start the server,

# We run a flask app defined at app.py with FLASK_APP=app.py flask run
# FLASK_APP must be set to the server file path with an equal sign in between. No spaces.
# FLASK_APP = app.py will not work. These flags have to be set exactly as expected, as FLAG=value.

# To enable live reload, set export FLASK_ENV=development in your terminal session to enable debug mode, prior to running flask run.
# Or call it together with flask run:
#   $ FLASK_APP=app.py FLASK_DEBUG=true flask run
# Alternative approach to run a Flask app: using __main__
# Instead of using $ flask run, we could have also defined a method

#   if __name__ == '__main__':
#     app.run()
# at the bottom of our app.py script, and then called $ python3 app.py in our terminal to invoke app.run() and run the flask app this way.

# When we call a script this way, using $ python script.py, the script's __name__ gets set to __main__ by the Python interpreter, which then runs through executing all code found in the script. When it reaches the end, and finds if __name__ == 'main', it evaluates this to True and therefore calls app.run() at the end, running the Flask app.


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Person {self.id}, {self.name}>'

# In Python, __repr__ is a special method used to represent a class's objects as a string. __repr__ is called by the repr() built-in function. You can define your own string representation of your class objects using the __repr__ method. Special methods are a set of predefined methods used to enrich your classes.

db.create_all()

person = Person.query.first()

@app.route('/')
def index():
    return 'Hello ' + person.name + '!'

@app.route('/anna')
def index2():
    return 'Hello Anna!'

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )