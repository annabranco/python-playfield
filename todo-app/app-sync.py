# HANDLES DATA SYNCHRONOUSLY

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///temp'
db = SQLAlchemy(app)

class Todos(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  def __repr__(self):
    return f'<Todo: {self.id} => {self.description}>'

db.create_all()

@app.route('/')
def index():
  # Query param => endpoint?temp=hello
  # value = request.args.get('temp')
  # Query param is sent by the GET post

  # Input form
  # value = request.form.get('temp')

  # Query param => endpoint?temp=hello
  # Received by the POST post
  # value_string = request.data
  # value = json.loads(value_string)

  return render_template('index.html', data=Todos.query.all())

@app.route('/todos/create', methods=['POST'])
def create():
  # POST method should be authorized as above
  value = request.form.get('description', '') # default '' if nothing comes from 'description'

  # request.form handles the data synchronously
  print(value)
  newTodo = Todos(description=value)
  db.session.add(newTodo)
  db.session.commit()

  # Form data is sent by POST method
  # value = request.args.get('temp')

  return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )