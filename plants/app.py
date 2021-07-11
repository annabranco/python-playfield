from flask import Flask, jsonify, request
from models import setup_db, Plant
from flask_cors import CORS, cross_origin
import math

app = Flask(__name__)
app.config.from_object('config')
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

@app.route('/plants')
def index():
  plants = Plant.query.all()
  formatted_plants = [plant.format() for plant in plants]
  page = request.args.get('page', 1, type=int)
  num_for_page = request.args.get('num', 10, type=int)
  initial = (page - 1) * num_for_page
  final = initial + num_for_page

  return jsonify(
    {
      'success': True,
      'data': formatted_plants[initial:final],
      'total_items': len(formatted_plants),
      'items_per_page': num_for_page,
      'total_pages': math.ceil(len(formatted_plants) / num_for_page),
    }
  )

if __name__ == '__main__':
    app.run()