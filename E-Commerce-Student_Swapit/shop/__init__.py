from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '328da185ded333072c92d78ece5023329cb4e25b40360af0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1772582:rbrokenshaw123@csmysql.cs.cf.ac.uk:3306/c1772582'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes