import sqlite3 
from flask import Flask, render_template, url_for
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id): 
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
        (post_id)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from forms import RegistrationForm, LoginForm

@app.route("/")
@app.route("/home")
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close() 
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route('<int: post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)