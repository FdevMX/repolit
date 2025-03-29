from flask import Flask

app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Import routes or controllers
from backend.controllers import auth_controller, file_controller, category_controller

if __name__ == '__main__':
    app.run(debug=True)