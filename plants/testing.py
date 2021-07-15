import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, request

from models import setup_db, Plant
from app import create_app

class PlantsTest(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "plantsdb_test"
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format('annabranco', 'pwd','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_plant = {
            'name': 'Anya',
            'scientific_name': 'Annya Arbolis',
            'is_poisonous': False,
            'primary_color': 'green'
        }
        self.new_plant_bad_data = {
            'name': 'Anya',
            'scientific_name': '',
            'is_poisonous': False,
            'primary_color': 'green'
        }
        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_root_redirects(self):
        """Redirects to valid page when trying to access root url"""
        res = self.client().get('/', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        res = self.client().get('/', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_get_plants(self):
        """[GET:/plants] accessed successfully"""
        res = self.client().get('/plants')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_a_single_plant(self):
        """[GET:/plants] accessed successfully"""
        res = self.client().get('/plants/1')
        data = json.loads(res.data)
        plant = Plant.query.first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['plant']['name'], plant.name)

    def test_get_a_nonexistent_plant(self):
        """[GET:/plants] returns 404 when plant is not found"""
        res = self.client().get('/plants/9999')
        data = json.loads(res.data)
        plant = Plant.query.first()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Not Found')

    def test_get_plants_paginated(self):
        """[GET:/plants] Returns the 10 first plants on basic get"""
        res = self.client().get('/plants')
        data = json.loads(res.data)
        self.assertGreaterEqual(data['total_items'], 12)
        self.assertGreaterEqual(data['total_pages'], 2)
        self.assertEqual(len(data['plants']), 10)
        self.assertEqual(data['plants'][0]['id'], 1)
        self.assertEqual(data['plants'][-1]['id'], 10)

    def test_get_plants_paginated_last_page(self):
        """[GET:/plants?page=2] Returns the last two plants"""
        res = self.client().get('/plants?page=2')
        data = json.loads(res.data)
        self.assertGreaterEqual(data['total_items'], 12)
        self.assertGreaterEqual(len(data['plants']), 2)
        self.assertEqual(data['plants'][0]['id'], 11)
        self.assertGreaterEqual(data['plants'][-1]['id'], 12)

    def test_get_plants_paginated_page_100(self):
        """[GET:/plants?page=100] Returns 404 if page requested does not exist"""
        res = self.client().get('/plants?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Not Found')

    def test_get_plants_paginated_by_3(self):
        """[GET:/plants?num=3] returns pagination with 3 plants"""
        res = self.client().get('/plants?num=3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['total_items'], 12)
        self.assertGreaterEqual(data['total_pages'], 4)
        self.assertEqual(len(data['plants']), 3)

    def test_get_plants_paginated_by_2_page_6(self):
        """[GET:/plants?num=2&page=6] returns 2 plants"""
        res = self.client().get('/plants?num=2&page=6')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['total_items'], 12)
        self.assertGreaterEqual(data['total_pages'], 6)
        self.assertEqual(len(data['plants']), 2)
        self.assertEqual(data['plants'][0]['id'], 11)
        self.assertEqual(data['plants'][-1]['id'], 12)

    def test_get_plants_paginated_by_0(self):
        """[GET:/plants?num=0] returns 400"""
        res = self.client().get('/plants?num=0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Bad Request')

    def test_create_plant_correct(self):
        """[POST:/plants] with correct body creates a plant"""
        res = self.client().post('/plants', json=self.new_plant)
        data = json.loads(res.data)
        plant = Plant.query.order_by(-Plant.id).first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertEqual(plant.name, self.new_plant['name'])

    def test_create_plant_incomplete(self):
        """[POST:/plants] with missing data body returns 400"""
        res = self.client().post('/plants', json=self.new_plant_bad_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Bad Request')

    def test_create_plant_incorrect(self):
        res = self.client().post('/plants')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Bad Request')

    def test_update_plant_one_attribute_correct(self):
        name = 'Ivy'
        last_plant = Plant.query.order_by(-Plant.id).first()
        print(f'$$$ last_plant: {last_plant.id}')

        res = self.client().patch(f'/plants/{last_plant.id}', json={ 'name': name })
        data = json.loads(res.data)
        print(f'$$$ data: {data}')


        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['id'], last_plant.id)
        self.assertEqual(data['updated']['name'], name)

    def test_update_plant_all_attributes_correct(self):
        name = 'Mushroom'
        scientific_name = 'I dont know'
        is_poisonous = True
        primary_color = 'red'

        last_plant = Plant.query.order_by(-Plant.id).first()
        print(f'$$$ last_plant: {last_plant.id}')

        res = self.client().patch(f'/plants/{last_plant.id}', json={
            'name': name,
            'scientific_name': scientific_name,
            'is_poisonous': is_poisonous,
            'primary_color': primary_color
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['id'], last_plant.id)
        self.assertEqual(data['updated']['name'], name)
        self.assertEqual(data['updated']['scientific_name'], scientific_name)
        self.assertEqual(data['updated']['is_poisonous'], is_poisonous)
        self.assertEqual(data['updated']['primary_color'], primary_color)

    def test_update_plant_attributes_does_not_change(self):
        first_plant = Plant.query.first()

        res = self.client().patch('/plants/1', json={ 'name': first_plant.name })
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 202)
        self.assertFalse(data['updated'])
        self.assertEqual(data['message'], 'Data not changed')

    def test_update_plant_incomplete(self):
        res = self.client().patch(f'/plants/1')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 'Unprocessable Entity')

    def test_update_plant_incorrect(self):
        res = self.client().patch('/plants/1', json={ 'Anya': 'Anya' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Bad Request')

    def test_update_plant_bad_endpoint(self):
        res = self.client().patch('/plants', json={ 'name': 'Anya' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Method not Allowed')

    def test_update_plant_nonexistent(self):
        res = self.client().patch('/plants/9999', json={ 'name': 'Anya' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Not Found')

    def test_delete_plant_correct(self):
        last_plant = Plant.query.order_by(-Plant.id).first()

        res = self.client().delete(f'/plants/{last_plant.id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], last_plant.id)

    def test_delete_plant_nonexistent(self):
        res = self.client().delete('/plants/999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Not Found')

    def test_delete_plant_bad_endpoint(self):
        res = self.client().delete('/plants')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Method not Allowed')

if __name__ == "__main__":
    unittest.main()