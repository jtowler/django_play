from flask import Flask, render_template
from flask_script import Manager, Command, Shell

app = Flask(__name__)
app.debug = True
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


def shell_context():
    import os
    import sys
    return dict(app=app, os=os, sys=sys)


manager.add_command("shell", Shell(make_context=shell_context))
if __name__ == "__main__":
    manager.run()
