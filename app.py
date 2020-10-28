from flask import Flask,jsonify, Response, request
import math
import hashlib
import requests
from redis import Redis, RedisError


#--------------instantiate the Flask object--------------#
app = Flask(__name__)

#URL used for Slack bot
SLACK_URL = 'https://hooks.slack.com/services/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'

#--------------Adding Redis application--------------#
redis = Redis(host="redis", socket_connect_timeout=2, socket_timeout=2)

#--------------Adding Redis data storage object template--------------#


#--------------App Routes--------------#
@app.route("/")
def index():
	return "Welcome to the Project 5 API"

#--------------md5 hash converter--------------#
@app.route('/md5/<string:input>', methods=['GET'])
def get_md5(input):
	res = hashlib.md5(input.encode())
	return jsonify(input=input,output=str(res.hexdigest()))

#--------------factorial converter--------------#
@app.route('/factorial/<int:n>')
def factorial(n):
    res1 = math.factorial(n)
    return jsonify(input=n, output=res1)


#--------------fibonacci endpoint--------------#
@app.route('/fibonacci/<int:n>', methods=['GET'])
def fib(n):
    a, b = 0, 1
    array = [0]
    while b <= n:
        array.append(b)
        a, b = b, a+b

    if n<=0:
        print("Incorrect input, please put a positive number")
    
    else:

        return jsonify(input=n, output=array)

#--------------prime endpoint--------------#
@app.route('/is-prime/<int:n>')
def prime_check(n):
    if n > 1: 
        for i in range(2, n):
            if (n % i) == 0:
                x = "False"
                break
                
        else:
            x = "True"

        return jsonify(input=n, output=x)


@app.route('/keyval/<string>')
#--------------slack alert endpoint--------------#
@app.route('/slack-alert/<string:x>')
def slack_post(x):
    data = { 'text' : x }
    resp = requests.post(SLACK_URL, json=data)
    if resp.status_code == 200:
        result = True
        verification = "Your message was sent succesfully."
    else:
        result = False
        verification = "Unable to post your message."
    return jsonify(
    input=x,
    message=verification,
    output=result
    ), 200 if resp.status_code==200 else 400


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
