from flask import Flask, jsonify, request, abort, redirect, url_for, make_response
from models import db, setup_db, Plant
from flask_cors import CORS, cross_origin
import math
from config import database_path

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)

    def is_invalid(attribute):
        return True if attribute is None or attribute == '' else False

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

# [C]RUD
    @app.route('/plants', methods=['POST'])
    def create_plant():
        try:
            name = request.get_json()['name']
            scientific_name = request.get_json()['scientific_name']
            is_poisonous = request.get_json()['is_poisonous']
            primary_color = request.get_json()['primary_color']

            if is_invalid(name) or is_invalid(scientific_name) or is_invalid(is_poisonous) or is_invalid(primary_color):
                abort(400)

            new_plant = Plant(name=name, scientific_name=scientific_name, is_poisonous=is_poisonous, primary_color=primary_color)
            new_plant.insert()

            return jsonify({
                'success': True,
                'created': new_plant.id,
            })
        except:
            db.session.rollback()
            abort(400)

        finally:
            db.session.close()

# C[R]UD
    @app.route('/plants')
    def index():
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        page = request.args.get('page', 1, type=int)
        num_for_page = request.args.get('num', 10, type=int)
        initial = (page - 1) * num_for_page
        final = initial + num_for_page

        if (num_for_page == 0):
            abort(400)

        if len(formatted_plants[initial:final]) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'plants': formatted_plants[initial:final],
            'total_items': len(formatted_plants),
            'items_per_page': num_for_page,
            'total_pages': math.ceil(len(formatted_plants) / num_for_page),
        })

    @app.route('/plants/<int:plant_id>', methods=['GET'])
    def get_plant(plant_id):
        try:
            plant = Plant.query.filter(Plant.id == plant_id).one_or_none() or 'n/a'

            if plant == 'n/a':
                abort(404)
            if plant:
                return jsonify({
                    'success': True,
                    'plant': plant.format()
                })
        except:
            abort(422)

# CR[U]D
    @app.route('/plants/<int:plant_id>', methods=['PATCH'])
    def update_plant(plant_id):
        if plant_id is None:
            abort(400)
        body = request.get_json()
        updated = False

        if body:
            for key in body:
                if key not in ('name', 'scientific_name', 'is_poisonous', 'primary_color'):
                    abort(400)

        try:
            plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
            if plant is None:
                abort(404)

            if 'name' in body:
                request_name = body.get('name')

                if request_name != '':
                    if request_name != plant.name:
                        plant.name = body.get('name')
                        updated = True
                else:
                    abort(422)

            if 'scientific_name' in body:
                request_scientific_name = body.get('scientific_name')
                if request_scientific_name != '':
                    if request_scientific_name != plant.scientific_name:
                        plant.scientific_name = body.get('scientific_name')
                        updated = True
                else:
                    abort(422)

            if 'is_poisonous' in body:
                request_is_poisonous = body.get('is_poisonous')
                if isinstance(body.get('is_poisonous'), bool):
                    if request_is_poisonous != plant.is_poisonous:
                        plant.is_poisonous = body.get('is_poisonous')
                        updated = True
                else:
                    abort(422)

            if 'primary_color' in body:
                request_primary_color = body.get('primary_color')
                if request_primary_color != '':
                    if request_primary_color != plant.primary_color:
                        plant.primary_color = body.get('primary_color')
                        updated = True
                else:
                    abort(422)

            if updated:
                plant.update()
                return jsonify({
                    'success': True,
                    'updated': plant.format(),
                })

            else:
                return make_response(jsonify({
                    'success': True,
                    'updated': False,
                    'message': 'Data not changed'
                }), 202)

        except:
            abort(422)

# CRU[D]
    @app.route('/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        try:
            if plant_id is None:
                abort(400)

            plant = Plant.query.filter(Plant.id == plant_id).one()

            plant.delete()

            return jsonify({
                'success': True,
                'deleted': plant_id,
            })

        except:
            abort(404)


    @app.route('/')
    def redirect_to_plants():
        return redirect(url_for('index'))

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'success': False,
        'error_code': 400,
        'error': 'Bad Request',
        'message': 'Your request cannot be processed because it is not correct or you are asking for null data'
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
        'success': False,
        'error_code': 403,
        'error': 'Forbidden',
        'message': 'You cannot access the root of this URL. Are you trying to access /plant path?'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error_code': 404,
        'error': 'Not Found',
        'message': 'Resource not found on database'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        'success': False,
        'error_code': 405,
        'error': 'Method not Allowed',
        'message': 'Are you handling the correct endpoint?'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'success': False,
        'error_code': 422,
        'error': 'Unprocessable Entity',
        'message': 'Your request could nor be processed. Are you sure your request is correct?'
        }), 422

    return app
