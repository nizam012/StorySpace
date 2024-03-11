from re import template
from tokenize import String
from flask import Flask, app, redirect, request, flash, session, jsonify, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import (
    login_manager,
    login_user,
    login_required,
    current_user,
    LoginManager,
    logout_user,
)
from flask_login import UserMixin
import os
import datetime
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
from flask_mail import Mail, Message  # Import Mail and Message from flask_mail

app = Flask(__name__, template_folder="templates")
# app.secret_key = secrets.token_hex(16)  # Generates a 16-byte (32-character) hex string
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Set SameSite attribute to None
# app.config['SESSION_COOKIE_SECURE'] = True  # Ensure the session cookie is secure (HTTPS)

# # Initialize session
# # app.secret_key = 'your_secret_key'  # Add your secret key here
# # Session(app)
app.secret_key = os.urandom(24)


# OTP Generator


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nizudin120@gmail.com'  # Set your email address here
app.config['MAIL_PASSWORD'] = 'daelmadeezmsxhah'  # Set your email password here

mail = Mail(app)  # Initialize Mail with the Flask app instance


# ... (rest of the code remains unchanged)
# Add this route to generate and send OTP via email
@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    email = request.json.get('email')

    # Generate a new OTP using the provided email
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    
    # Send OTP via email
    msg = Message('Your OTP for Verification', sender=app.config['MAIL_USERNAME'], recipients=[email])

    body = f'Your OTP is: {otp}'
    msg.body = body

    try:
        mail.send(msg)
        return jsonify({'message': 'OTP sent successfully'})
    except Exception as e:
        return jsonify({'message': f'Error sending OTP: {str(e)}'}), 500
  #END OF OTP


app.config["UPLOAD_FOLDER"] = (
    r"D:\Project\Learning_point\Learning_point\website\static\uploads"
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql://sql6689068:6f2ljfMrS2@sql6.freesqldatabase.com:3306/sql6689068?charset=utf8"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# class models for db tables user db.create_all() in python intrepture so that this call can create table
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64))
    phone = db.Column(db.String(10))
    password = db.Column(db.String(1024))


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))


class Books(db.Model, UserMixin):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_name = db.Column(db.String(60))
    seller_phone = db.Column(db.String(10))
    seller_address = db.Column(db.String(120))
    name = db.Column(db.String(75))
    category = db.Column(db.String(255))
    price = db.Column(db.String(50))
    auther = db.Column(db.String(100))
    des = db.Column(db.String(500))
    slug = db.Column(db.String(50))
    photo = db.Column(db.String(200))
    date = db.Column(db.DateTime)


class Invoice(db.Model, UserMixin):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_name = db.Column(db.String(60))
    book_name = db.Column(db.String(60))
    address = db.Column(db.String(60))
    email = db.Column(db.String(60))
    phone = db.Column(db.String(30))
    price = db.Column(db.String(30))
    upi = db.Column(db.String(60))
    card_no = db.Column(db.String(60))
    card_name = db.Column(db.String(60))
    cvv = db.Column(db.String(60))
    expire = db.Column(db.String(60))
    date = db.Column(db.Date)
    # important
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    User = db.relationship("User", backref=db.backref("user", order_by=id), lazy=True)

# log-out model
@app.route("/home")
@login_required
def home():
    books = Books.query.all()
    return render_template("home.html", books=books)


@app.route("/search", methods=["GET", "POST"])
def search():
    item = request.form.get("search")
    search = Books.query.filter_by(name=item).all()

    if search:
        return render_template("search.html", books=search)
    else:
        search = Books.query.filter_by(auther=item).all()
        return render_template("search.html", books=search)


@app.route("/purchase/<int:id>", methods=["GET", "POST"])
@login_required
def purchase(id):
    books = Books.query.filter_by(id=id).first()
    my_id = current_user.get_id()
    current = User.query.filter_by(id=my_id).first()
    return render_template("purchase.html", book=books, user=current)


@app.route("/purchase/invoice/<int:id>", methods=["GET", "POST"])
def invoice(id):
    books = Books.query.filter_by(id=id).first()
    my_id = current_user.get_id()
    user = User.query.filter_by(id=my_id).first()
    if request.method == "POST":
        upi = request.form.get("upi")
        card_holder = request.form.get("cname")
        card_number = request.form.get("cnumber")
        card_exp = request.form.get("cexp")
        card_cvv = request.form.get("ccv")
        name = request.form.get("fname")
        address = request.form.get("desc")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if upi:
            invoice = Invoice(
                purchase_name=name,
                book_name=books.name,
                address=address,
                email=email,
                phone=phone,
                upi=upi,
                user_id=my_id,
                price=books.price,
                date=datetime.datetime.now(),
            )
            db.session.add(invoice)
            db.session.commit()
            data = Invoice.query.filter_by(id=my_id).first()
            return render_template("invoice.html", book=books, data=data, date=datetime)

        elif card_number:   
            invoice = Invoice(
                purchase_name=name,
                book_name=books.name,
                address=address,
                email=email,
                phone=phone,
                card_name=card_holder,
                card_no=card_number,
                cvv=card_cvv,
                expire=card_exp,
                date=datetime.datetime.now(),
                user_id=my_id,
                price=books.price,
            )
            db.session.add(invoice)
            db.session.commit()

            data = Invoice.query.filter_by(id=my_id).first()
            return render_template("invoice.html", book=books, data=data, date=datetime)
        else:
            flash("Enter upi or card", category="error")

    return render_template("invoice.html", book=books, user=user)


@app.route("/purchased", methods=["GET", "POST"])
def cart():
    my_id = current_user.get_id()
    pur = Invoice.query.filter_by(user_id=my_id).all()
    date = datetime.datetime.now()
    return render_template("/purchased.html", books=pur)


# delete model
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    user = User.query.filter_by(id=id).first()
    book = Books.query.filter_by(id=id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Book Removed", category="error")
    else:
        db.session.delete(user)
        db.session.commit()
        flash("User Removed", category="error")
    return redirect("/admin")


@app.route("/")
def front():
    books = Books.query.all()
    return render_template("front_page.html", books=books)


@app.route("/book/<string:book_slug>", methods=["GET"])
def book_get(book_slug):
    book = Books.query.filter_by(slug=book_slug).first()
    return render_template("book_page.html", book=book)


@app.route("/admin")
def admin():
    users = User.query.all()
    admin = Admin.query.all()
    books = Books.query.all()
    return render_template("admin.html", users=users, books=books, admin=admin)


# this is login model
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=email).first()
        user = User.query.filter_by(email=email).first()

        if admin:
            if admin.password == password:
                return redirect("/admin")
            else:
                flash("Incorrect Password", category="error")
        elif user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect("/home")
            else:
                flash("Incorrect password, try again.", category="error")
        elif email == null:
            flash("Enter the email and Password", category="error")
        else:
            flash("Enter valid email and Password to Login", category="error")
            return render_template("login.html", user=current_user)

    return render_template("login.html")

# this is log_out model
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# this is the sign up model
@app.route("/sign-up", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        phone = request.form.get("phonenumber")
        username = request.form.get("username")
        password = request.form.get("password")
        password1 = request.form.get("password1")

        # Additional checks for email already existing and OTP validation can go here
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please use a different email.", category="error")
            return render_template("sign_up.html")

        # Add more checks for OTP validation if needed

        if len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(username) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password != password1:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 4:
            flash("Password must be at least 7 characters.", category="error")
        elif len(phone) != 10:
            flash("Phone number must be 10 characters.", category="error")
        elif not phone.isdigit():
            flash("Phone number must have only numbers.", category="error")
        else:
            # user_otp = request.form.get("otp")  # Assuming OTP is entered in the form
            # stored_otp = session.get("otp")  # Retrieve OTP from session

            # if user_otp != stored_otp:
            #     flash("Invalid OTP. Please try again.", category="error")
            #     return render_template("sign_up.html")
            # OTP matched, proceed with registration
            hashed_password = generate_password_hash(password)
            data = User(
                username=username,
                email=email,
                phone=phone,
                password=hashed_password,
            )
            db.session.add(data)
            db.session.commit()
            return redirect("/login")

    return render_template("sign_up.html")

@app.route("/seller", methods=["GET", "POST"])
def seller():
    s = 20
    if request.method == "POST":
        files = request.files["image"]

        if not files:
            flash("Image not uploaded.", category="error")
            return redirect("/seller")

        files.save(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(files.filename))
        )
        filename = secure_filename(files.filename)
        seller_name = request.form.get("uname")
        seller_phone = request.form.get("phoneNumber")
        seller_address = request.form.get("address")
        book_name = request.form.get("nameb")
        category = request.form.get("category")
        book_desc = request.form.get("desc")
        author = request.form.get("author")
        price = request.form.get("price")
        date = datetime.datetime.now()

        if len(seller_phone) < 10:
            flash("Phone number must be at least 10 characters.", category="error")
        elif len(seller_phone) > 10:
            flash("Phone number must be 10 characters.", category="error")
        elif seller_phone == String:
            flash("Phone number must have only numbers", category="error")
        else:
            ran = "".join(
                random.choices(
                    string.ascii_uppercase
                    + string.ascii_lowercase
                    + book_name
                    + string.digits,
                    k=s,
                )
            )

            data = Books(
                seller_name=seller_name,
                seller_phone=seller_phone,
                seller_address=seller_address,
                name=book_name,
                category=category,
                des=book_desc,
                auther=author,
                price=price,
                photo=filename,
                slug=ran,
                date=date,
            )

            db.session.add(data)
            db.session.commit()
            return redirect("/home")

    return render_template("seller_form.html")


if __name__ == "__main__":
    app.run(debug=True)