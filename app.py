import flask

app = flask.Flask(__name__)

# This function takes a greeting from the url path
# And a name from the query string to greet user
@app.route('/greet/<greeting>', methods=['GET'])
def greet(greeting):
    # Get /hello?key=value&name=Rita
    # query = {"key: "value", "name": "Rita"} 
    query = flask.request.args 
    res = flask.make_response("%s %s" %(greeting, query.get('name')))
    res.headers['Content-type'] = 'text'
    return res

# This function returns the profile image from server
@app.route('/profile', methods=['GET'])
def profile():
    return flask.send_file('public/profile.jpg')