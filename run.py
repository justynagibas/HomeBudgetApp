from app import app
from app.database.database import create_tables

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)