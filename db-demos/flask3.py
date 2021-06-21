from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DDL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    fav_color = db.Column(db.String())
    age = db.Column(db.Integer())
    def __repr__(self):
        return f'<Person {self.id}, {self.name}, {self.age}, {self.fav_color}>'

db.create_all()


@app.route('/')
def index():
    userOne = Users.query.first()
    if (userOne):
        return 'Hello ' + userOne.name + '!'
    else:
        user1 = Users(name='Anya', fav_color='green', age=39)
        user2 = Users(name='Krys', fav_color='rainbow', age=26)

        allUsers = [user1, user2]

        for user in allUsers:
            userExists = len(Users.query.filter(Users.name == user.name).all()) > 0
            if not userExists:
                db.session.add(user)

        db.session.commit()

        print(Users.query.all())

        return 'Hello stranger'

@app.route('/del')
def index2():
    print(Users.query.all())
    Users.query.delete()
    db.session.commit()

    return 'Everything is blown up!'

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )