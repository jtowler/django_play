from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_script import Manager, Command, Shell
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import ContactForm

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flask_app_db'

manager = Manager(app)
db = SQLAlchemy(app)


class Faker(Command):
    """blah"""

    def run(self):
        print('fake date entered')


manager.add_command('faker', Faker())


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)


@manager.command
def foo():
    """blaaaa"""
    print('foo executed')


@app.route('/')
def index():
    return render_template('index.html', name='Jerry')


@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)


@app.route('/books/<genre>/')
def books(genre):
    return "All Books in {} category".format(genre)


@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('password')

        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"

    return render_template('login.html', message=message)


@app.route('/contact/', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(name)
        print(email)
        print(message)
        # db logic goes here
        print("\nData received. Now redirecting ...")
        flash("Message Received", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response('Setting a cookie')
        res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(f"Value of cookie foo is {request.cookies.get('foo')}")
    return res


@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response('Cookie removed')
    res.set_cookie('foo', 'bar', max_age=0)
    return res


@app.route('/article/', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
        res.headers['location'] = url_for('article')
        return res, 302

    return render_template('article.html')


@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1  # setting session data
    return "Total visits: {}".format(session.get('visits'))


@app.route('/session/')
def updating_session():
    res = str(session.items())

    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['pineapples'] = '100'
        session.modified = True
    else:
        session['cart_item'] = cart_item

    return res


@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # delete visits
    return 'Visits deleted'


def shell_context():
    import os
    import sys
    return dict(app=app, os=os, sys=sys)


manager.add_command("shell", Shell(make_context=shell_context))
if __name__ == "__main__":
    manager.run()
