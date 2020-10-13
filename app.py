from flask import Flask,jsonify, Response

#instantiate the Flask object
app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome to the Project 5 API"

if __name__ == '__main__':
	app.run(debug=True)
