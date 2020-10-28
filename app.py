from flask import Flask,jsonify, Response, request
import math
import hashlib
import json
import requests
from redis import Redis, RedisError
import redis
from collections import defaultdict


#--------------instantiate the Flask object--------------#
app = Flask(__name__)

#URL used for Slack bot
SLACK_URL = 'https://hooks.slack.com/services/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'

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

#--------------Project 6 Continuation Redis--------------#
#Adding the Redis port
red = redis.Redis(host='redis', port=6379, db=0)

#app route to POST & PUT
@app.route('/keyval', methods=['POST', 'PUT'])
def key_values():
   #Returning format for the json vals
    json_values = {
        #string
        'key': None,
        #string
        'value': None,
        #string
        'command': 'CREATE' if request.method=='POST' else 'UPDATE',
        #bool
        'result': False,
        #string
        'error': None
    }
#  This code will check to see if it connects to redis
    try:
        testing_value = red.get(json_values['key'])
    except RedisError:
        json_values['error'] = "Problems connecting to redis."
        return jsonify(json_values), 400
#This code checks to see if theres already a keyval
    if request.method == 'POST' and not testing_value == None:
        json_values['error'] = "Unable to create new records: key already exists."
        return jsonify(json_values), 409
#This code will check if the value exist
    elif request.method == 'PUT' and testing_value == None:
        json_values['error'] = "Unable to update records: key does not exist."
        return jsonify(json_values), 404
#This code checks if any values are made in redis or being a success
    elif red.set(json_values['key'], json_values['value']) == False:
        json_values['error'] = "Error: problem creating the value in Redis."
        return jsonify(json_values), 400
    else:
        json_values['result'] = True
        return jsonify(json_values), 200

#App route to GET & DELETE
@app.route('/keyval/<string:key>', methods=['GET', 'DELETE'])
def key_value_retrieve(key):
    #Returning format for the json vals
    json_values = {
        'key': key,
        'value': None,
        'command': "{} {}".format('RETRIEVE' if request.method=='GET' else 'DELETE', key),
        'result': False,
        'error': None
    }
    ##  This code will check to see if it connects to redis
    try:
        testing_value = red.get(key)
    except RedisError:
        json_values['error'] = "Error: unable to connect to redis."
        return jsonify(json_values), 400
    #This code will check if the value exist
    if testing_value == None:
        json_values['error'] = "Error: key do not exist."
        return jsonify(json_values), 404
    else:
        json_values['value'] = testing_value
    #This code will get the key results
    if request.method == 'GET':
        json_values['result'] = True
        return jsonify(json_values), 200
    #This code will delete key values
    elif request.method == 'DELETE':
        ret = red.delete(key)
        if ret == 1:
            json_values['result'] = True
            return jsonify(json_values)
        else:
            json_values['error'] = "Error: can not delete key (expected return value 1; client returned {ret})"
            return jsonify(json_values), 400


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
