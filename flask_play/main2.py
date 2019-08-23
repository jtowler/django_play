from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def requestdata():
    return f"Your IP is {request.remote_addr} and you are using {request.user_agent}"


@app.route('/a')
def http_404_handler():
    return make_response("<h2>404 Error</h2>", 400)


@app.route('/set-cookie')
def set_cookie():
    res = make_response("Cookie setter")
    res.set_cookie("favorite-color", "skyblue", 60*60*24*15)
    res.set_cookie("favorite-font", "sans-serif", 60*60*24*15)
    return res


@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return f'Profile Page of user #{user_id}'


@app.route('/books/<genre>/')
def books(genre):
    res = make_response("All Books in {} category".format(genre))
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'Foobar'
    return res


if __name__ == "__main__":
    app.run(debug=True)
