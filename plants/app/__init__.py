from flask import Flask, jsonify, request, abort, redirect, url_for
from models import setup_db, Plant
from flask_cors import CORS, cross_origin
import math
from config import database_path

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app, database_path)
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

        if len(formatted_plants[initial:final]) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'plants': formatted_plants[initial:final],
            'total_items': len(formatted_plants),
            'items_per_page': num_for_page,
            'total_pages': math.ceil(len(formatted_plants) / num_for_page),
        })

    @app.route('/plants/<int:plant_id>')
    def get_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)

        return jsonify({
            'success': True,
            'data': plant.format()
        })

    @app.route('/')
    def redirect_to_plants():
        return redirect(url_for('index'))

    @app.errorhandler(403)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 403,
        'message': 'You cannot access the root of this URL. Are you trying to access /plant path?'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
        }), 404

    return app
