import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True

# Connect to the database
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'annabranco')
DB_PWD = os.getenv('DB_PWD', 'pwd')
DB_NAME = os.getenv('DB_NAME', 'plantsdb')

database_path = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'
