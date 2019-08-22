from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/career/')
def career():
    return 'Career Page'


@app.route('/user/<int:id>/')
def user_profile(id):
    return f'Profile Page of user #{id}'


@app.route('/contact/')
@app.route('/feedback/')
def feedback():
    return 'Feedback Page'


if __name__ == "__main__":
    app.run(debug=True)
