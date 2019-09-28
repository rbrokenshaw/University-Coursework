from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,8}$', message='Your password should be between 6 and 8 characters long.')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	university = StringField('University')
	address_house = StringField('House Number/Name', validators=[DataRequired()])
	address_street = StringField('Street Name')
	address_towncity = StringField('Town/City')
	address_postcode = StringField('Postcode', validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')


class BookSearchForm(FlaskForm):
	isbn = StringField('ISBN', validators=[DataRequired()])
	submitsell = SubmitField('Sell this book')

class AllBooksSearch(FlaskForm):
	search_term = StringField('Search all books', validators=[DataRequired()])
	submit = SubmitField('Search')

class SellBookForm(FlaskForm):
	isbn = StringField('ISBN', validators=[DataRequired()])
	title =  StringField('Title', validators=[DataRequired()])
	authors = StringField('Author(s)')
	publishers = StringField('Publisher(s)')
	category = StringField('Category')
	condition = SelectField('Please select the book condition', choices=[('as_new', 'As New'), ('fine', 'Fine'), ('very_good', 'Very Good'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')])
	defects = StringField('Please note any defects')
	price = DecimalField(places=2, rounding=None, use_locale=False, number_format=None)
	shipping = DecimalField(places=2, rounding=None, use_locale=False, number_format=None)
	cover = StringField('Cover Image')
	submit = SubmitField('Sell This Book')

class PaymentForm(FlaskForm):
	card_name = StringField('Name on Card', validators=[DataRequired()])
	card_number = IntegerField('Card Number', validators=[DataRequired()])
	card_expiry = StringField('Card Expiry', validators=[DataRequired()])
	card_cvv = IntegerField('CVV', validators=[DataRequired()])
	submit = SubmitField('Buy Now')

class SetUpPaymentForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	accountno = IntegerField('Account No', validators=[DataRequired()])
	sortcode = IntegerField('Sort Code', validators=[DataRequired()])
	submit = SubmitField('Confirm Details')

