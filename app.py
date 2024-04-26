import flask

app = flask.Flask(__name__)

@app.route('/hello', methods=['GET'])
def home():
    query = flask.request.args 
    # Get /hello?key=value&name=Rita
    # query = {"key: "value", "name": "Rita"} 
    return "Hello %s" %(query.get('name'))