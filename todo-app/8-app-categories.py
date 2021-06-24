# HANDLES DATA ASYNCHRONOUSLY USING HTTP

from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
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
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

  def __repr__(self):
    return f'<Todo: {self.id} => {self.description}>'

class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todos', backref='cat', lazy=True) # lazy=True is default

  def __repr__(self):
    return f'<Category: {self.id} => {self.description}>'

# [C]RUD
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
    print(sys.exc_info()) # for debugging, recording erorrs
  finally:
    db.session.close()

  if error:
    abort(400)
  else:
    # return jsonify(addedTodo)
    return redirect(url_for('index'))

# CR[U]D
@app.route('/todos/toggle/<id>', methods=['POST'])
def toggle(id):
  try:
    completed = request.get_json()['completed']
    todo = Todos.query.get(id)
    todo.completed = completed
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('index'))

# CRU[D]
@app.route('/todos/<id>', methods=['DELETE'])
def delete(id):
  try:
    todo = Todos.query.get(id)
    db.session.delete(todo)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return jsonify({ 'success': True })

# C[R]UD
@app.route('/all/')
def index_all():
  return render_template('index.html', data=Todos.query.order_by(Todos.completed, Todos.id.desc()).all())

@app.route('/category/<cat_id>')
def index_cat(cat_id):
  return render_template('index.html', data=Todos.query.filter_by(category_id=cat_id).order_by(Todos.completed, Todos.id.desc()).all())


@app.route('/')
def index():
  return redirect(url_for('index_cat', cat_id=1))


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )