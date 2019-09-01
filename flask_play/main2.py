from flask import Flask, render_template, request, redirect, url_for, flash
from flask_script import Manager, Command, Shell
from forms import ContactForm

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
manager = Manager(app)


class Faker(Command):
    """blah"""

    def run(self):
        print('fake date entered')


manager.add_command('faker', Faker())


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


def shell_context():
    import os
    import sys
    return dict(app=app, os=os, sys=sys)


manager.add_command("shell", Shell(make_context=shell_context))
if __name__ == "__main__":
    manager.run()
