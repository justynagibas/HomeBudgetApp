from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

db_url = "postgresql://postgres:postgres@localhost:5432/HomeBudget"

if not database_exists(db_url):
    create_database(db_url)

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url


db = SQLAlchemy(app)

from app.routes import routes