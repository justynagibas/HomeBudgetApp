from app import app
from flask import render_template
from app.database import database
from app.auth import auth

@app.route('/')
def index():
    return render_template('main_page.html')