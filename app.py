from flask import Flask,jsonify, Response, request
import math
import hashlib
import json
import requests
from redis import Redis, RedisError
import redis
from collections import defaultdict
from argparse import ArgumentParser
from pprint import pprint
import csv

#--------------instantiate the Flask object--------------#
app = Flask(__name__)


#URL used for Slack bot
SLACK_URL = 'https://hooks.slack.com/services/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'

#--------------App Routes--------------#
@app.route("/")
def index():
	return "Welcome to the Project API"

#--------------Project 6 Continuation Redis--------------#
#Adding the Redis port
red = redis.Redis(host='redis', port=6379, db=0)


@app.route('/keyval', methods=['POST'])
def test4():
    payload = request.get_json()
    key = payload['key']
    value = payload['value']
    if key in redis:
        JSON1 = {
         'key': key,
         'value': value, 
         'command': "CREATE: {}".format(key),
         'result': False,
         'error':"Unable to add pair key exists"
         }
        return JSON1, 404 

    else:
        redis.set(key, value), 200 

    JSON = {
         'key': key,
         'value': value, 
         'command': "CREATE: {}".format(key),
         'result': True
         }

    return JSON  


@app.route('/keyval', methods=['PUT'])
def test5():
    payload = request.get_json()
    key = payload['key']
    value = payload['value']
    if redis.exists(key):
        redis.set(key, value) 
        JSON1 = {
         'key': key,
         'value': value, 
         'command': "Update: {}".format(key),
         'result': True
         }
        return JSON1, 200 

    else:

        JSON = {
         'key': key,
         'value': value, 
         'command': "UPDATE: {}".format(key),
         'result': False,
         'error':"Unable to update key does not exist",
         }

    return JSON, 404 

@app.route('/keyval/<string:key>', methods=['GET'])
def key_value_retrieve(key):
    if key in redis:
        redis.get(key)
        JSON1 = {
         'key': key,
         'value': None, 
         'command': "Retrieve: {}".format(key),
         'result': True
         }
        return JSON1, 200 
    else:
        JSON = {
         'key': key,
         'value': None, 
         'command': "Retrieve: {}".format(key),
         'result': False,
         'error':"Unable to retrieve, key does not exist",
         }

    return JSON, 404 


@app.route('/keyval/<string:key>', methods=['DELETE'])
def key_value_delete(key):
    if key in redis:
        redis.delete(key)
        JSON1 = {
         'key': key,
         'value': None, 
         'command': "DELETE: {}".format(key),
         'result': True
         }
        return JSON1, 200 
    else:
        JSON = {
         'key': key,
         'value': None, 
         'command': "DELETE: {}".format(key),
         'result': False,
         'error':"Unable to retrieve, key does not exist",
         }

    return JSON, 404 

@app.route('/get', methods=['GET'])
def test2():
    return jsonify({'message' : 'It works!'})

	
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
    number = isinstance(n, int)
    if number == True:
        if n > 1: 
            for i in range(2, n):
                if (n % i) == 0:
                    return jsonify(input=n, output=False)
            return jsonify(input=n, output=True)
        elif(n == 0):
            return jsonify(input=n, output=False)            
        elif(n == 1):
            return jsonify(input=n, output=False)             
    else: 
        return jsonify(input=n, output=True)


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
