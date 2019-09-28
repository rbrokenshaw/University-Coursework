import os
from flask import render_template, url_for, request, redirect, flash, session, Markup
from shop import app, db
from shop.models import Book, User, BookSold, Payment
from shop.forms import RegistrationForm, LoginForm, BookSearchForm, SellBookForm, AllBooksSearch, PaymentForm, SetUpPaymentForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
	data = db.session.query(Book, User).join(User).order_by(User.id.desc())[:6]
	form = BookSearchForm()
	allbookssearchform = AllBooksSearch()
	if form.validate_on_submit():
		if form.submitsell.data:
			isbn = form.isbn.data
			return redirect (url_for('booksell', isbn=isbn))
	if allbookssearchform.validate_on_submit():
		search_term = allbookssearchform.search_term.data
		return redirect (url_for('booksearch', search_term=search_term))
	return render_template('home.html', data=data, title='Student Swap.it', form=form, allbookssearchform=allbookssearchform)

@app.route("/booksell<string:isbn>", methods=['GET', 'POST'])
def booksell(isbn):
	books = Book.query.all()
	form = SellBookForm()
	if form.validate_on_submit():
		if "id" not in session:
			flash(Markup('Please <a href="/login">login</a> or create an account below:'))
			return redirect('/register')
		else:
			seller_id = session['id']
			conditionFormatted = form.condition.data.replace("_", " ")
			conditionFormatted = conditionFormatted.capitalize()
			book = Book(title=form.title.data, category=form.category.data, isbn=form.isbn.data, publisher=form.publishers.data, condition=conditionFormatted, defects=form.defects.data, price=form.price.data, shipping=form.shipping.data, author=form.authors.data, cover=form.cover.data, seller_id=seller_id)
			db.session.add(book)
			db.session.commit()
			return redirect(url_for('home'))
	isbn = isbn.replace("-", "")
	return render_template('booksell.html', isbn=isbn, form=form,)

@app.route("/booksearch<string:search_term>", methods=['GET', 'POST'])
def booksearch(search_term):
	allbookssearchform = AllBooksSearch()
	if allbookssearchform.validate_on_submit():
		search_term = allbookssearchform.search_term.data
		results = Book.query.filter(Book.title.contains(search_term)).all()
		return redirect (url_for('booksearch', search_term=search_term))
	results = Book.query.filter(Book.title.contains(search_term)).all()
	return render_template('booksearch.html', search_term=search_term, results=results, allbookssearchform=allbookssearchform)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

# finish this
@app.route("/categories")
def categories():
	data = Book.query.all()
	categorylist = []
	for i in data:
		categorylist.append(i.category)
	for category in categorylist:
		pass
	return render_template('categories.html', categorylist=categorylist)

@app.route("/book/<int:book_id>")
def book(book_id):
	book = Book.query.get_or_404(book_id)
	user_id = book.seller_id
	user = User.query.get_or_404(user_id)
	return render_template('book.html', title=book.title, book=book, user=user)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data, university=form.university.data, address_house=form.address_house.data, address_street=form.address_street.data, address_towncity=form.address_towncity.data, address_postcode=form.address_postcode.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('welcome'))
	return render_template('register.html', title='Register', form=form)

@app.route("/welcome")
def welcome():
	return render_template('welcome.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			session['id'] = user.id
			return redirect(url_for('home'))
		else:
			flash("Sorry, your username or password is incorrect. Please try again.")
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	session.clear()
	logout_user()
	return redirect(url_for('home'))

@app.route('/user/<username>')
def user(username):
	if "id" not in session:
		logged_in_id = 0
	else:
		logged_in_id = session["id"]
	user = User.query.filter_by(username=username).first_or_404()
	seller_id = user.id
	booksforsale = Book.query.filter_by(seller_id=seller_id)
	bookssold = BookSold.query.filter_by(seller_id=seller_id)
	return render_template('user.html', user=user, booksforsale=booksforsale, bookssold=bookssold, logged_in_id=logged_in_id)

@app.route("/shipped/<int:book_id>")
def shipped(book_id):
	book = BookSold.query.filter_by(id=book_id).first_or_404()
	book.posted = True
	db.session.commit()
	return redirect(url_for('home'))

@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
	if "id" not in session:
		return redirect('/register')
	else:
		if "cart" not in session:
			session["cart"] = []
		session["cart"].append(book_id)
		flash("The book is added to your shopping cart!")
		return redirect("/cart")


@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
	if "cart" not in session:
		form = PaymentForm()
		flash('There is nothing in your cart.')
		return render_template("cart.html", display_cart = {}, total = 0, form=form)
	else:
		form = PaymentForm()
		items = session["cart"]
		cart = {}
		total_price = 0
		total_shipping = 0
		overall_total = 0
		total_quantity = 0
		for item in items:
			book = Book.query.get(item)

			total_price += book.price
			total_shipping += book.shipping
			overall_total = total_price + total_shipping
			if book.id in cart:
				cart[book.id]["quantity"] += 1
			else:
				seller = User.query.filter_by(id=book.seller_id).first()
				cart[book.id] = {"quantity":1, "title": book.title, "price":book.price, "shipping":book.shipping, "cover":book.cover, "seller_id":book.seller_id, "seller":seller.username}
			total_quantity = sum(item['quantity'] for item in cart.values())
		if form.validate_on_submit():
			for item in items:
				book_id = book.id
				book = Book.query.get_or_404(item)
				buyer_id = session['id']
				soldbook = BookSold(title=book.title, category=book.category, isbn=book.isbn, publisher=book.publisher, condition=book.condition, defects=book.defects, price=book.price, author=book.author, cover=book.cover, seller_id=book.seller_id, buyer_id=buyer_id, posted=False)
				db.session.add(soldbook)
				Book.query.filter_by(id=book.id).delete()
				db.session.commit()
				session["cart"] = []
			return redirect("/paymentcomplete")
		return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_shipping=total_shipping, total_quantity = total_quantity, overall_total = overall_total, form=form)
	return render_template('cart.html')

@app.route("/paymentcomplete")
def payment_complete():
	return render_template("payment_complete.html")

@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
	if "cart" not in session:
		session["cart"] = []

	session["cart"].remove(book_id)

	flash("The book has been removed from your shopping cart!")

	session.modified = True

	return redirect("/cart")

@app.route("/payment", methods=['GET', 'POST'])
def payment():
	form = SetUpPaymentForm()
	username = current_user.username
	if form.validate_on_submit():
		payment = Payment(username=username, firstname=form.firstname.data, lastname=form.lastname.data, accountno=form.accountno.data, sortcode=form.sortcode.data)
		db.session.add(payment)
		db.session.commit()
		return redirect("/payment_setup_complete")
	return render_template("payment.html", form=form)

@app.route("/payment_setup_complete")
def payment_setup_complete():
	return render_template("payment_setup_complete.html")

