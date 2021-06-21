# HANDLES DATA ASYNCHRONOUSLY USING HTTP

from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todos(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)

  def __repr__(self):
    return f'<Todo: {self.id} => {self.description}>'

# db.create_all() # since we are using Migration, we no longer use create_all()

@app.route('/')
def index():

  return render_template('index.html', data=Todos.query.all())

@app.route('/todos/create', methods=['POST'])
def create():
  error = False
  addedTodo = {}

  try:
    print(request.get_json())
    todo = request.get_json()['description']
    newTodo = Todos(description=todo)
    db.session.add(newTodo)
    db.session.commit()
    addedTodo['description'] = newTodo.description
  except:
    error = True
    db.session.rollback()
   # print(sys.exc_info()) # for debugging, recording erorrs
  finally:
    db.session.close()

  if error:
    abort(400)
  else:
    return jsonify(addedTodo)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )