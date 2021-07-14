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
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format('annabranco', '***','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        self.new_plant = {
            'name': 'Anya',
            'scientific_name': 'Annya Arbolis',
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


    def test_get_plants_paginated(self):
        """[GET:/plants] Returns the 10 first plants on basic get"""
        res = self.client().get('/plants')
        data = json.loads(res.data)
        self.assertEqual(data['total_items'], 12)
        self.assertEqual(data['total_pages'], 2)
        self.assertEqual(len(data['plants']), 10)
        self.assertEqual(data['plants'][0]['id'], 1)
        self.assertEqual(data['plants'][-1]['id'], 10)

    def test_get_plants_paginated_last_page(self):
        """[GET:/plants?page=2] Returns the last two plants"""
        res = self.client().get('/plants?page=2')
        data = json.loads(res.data)
        self.assertEqual(data['total_items'], 12)
        self.assertEqual(len(data['plants']), 2)
        self.assertEqual(data['plants'][0]['id'], 11)
        self.assertEqual(data['plants'][-1]['id'], 12)

    def test_get_plants_paginated_page_100(self):
        """[GET:/plants?page=100] Returns 404 if page requested does not exist"""
        res = self.client().get('/plants?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_plants_paginated_by_3(self):
        """[GET:/plants?num=3] returns pagination with 3 plants"""
        res = self.client().get('/plants?num=3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_items'], 12)
        self.assertEqual(data['total_pages'], 4)
        self.assertEqual(len(data['plants']), 3)

    def test_get_plants_paginated_by_2_last_page(self):
        """[GET:/plants?num=2&page=6] returns last 2 plants"""
        res = self.client().get('/plants?num=2&page=6')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_items'], 12)
        self.assertEqual(data['total_pages'], 6)
        self.assertEqual(len(data['plants']), 2)
        self.assertEqual(data['plants'][0]['id'], 11)
        self.assertEqual(data['plants'][-1]['id'], 12)

    def test_get_plants_paginated_by_0(self):
        """[GET:/plants?num=0] returns 400"""
        res = self.client().get('/plants?num=0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# TODO: keep on tests
# All CRUD

if __name__ == "__main__":
    unittest.main()