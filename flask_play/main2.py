from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def requestdata():
    return f"Your IP is {request.remote_addr} and you are using {request.user_agent}"


@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return f'Profile Page of user #{user_id}'


@app.route('/books/<genre>/')
def books(genre):
    return f'All books in {genre} category'


if __name__ == "__main__":
    app.run(debug=True)
