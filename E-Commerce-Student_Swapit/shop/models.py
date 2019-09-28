
from datetime import datetime
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(100), nullable=False)
    defects = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    shipping = db.Column(db.Numeric(10,2), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    cover = db.Column(db.String(100))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}', '{self.price}')"

class BookSold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(100), nullable=False)
    defects = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    cover = db.Column(db.String(100))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posted = db.Column(db.Boolean, nullable=False, default=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    university = db.Column(db.String(100), nullable=True)
    address_house = db.Column(db.String(50), nullable=False)
    address_street = db.Column(db.String(100), nullable=True)
    address_towncity = db.Column(db.String(50), nullable=True)
    address_postcode = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('user.username'), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    accountno = db.Column(db.Integer, nullable=False)
    sortcode = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

