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
@data_class
class JsonResponse():
    key: str = None
    value: str = None
    command: str = None
    result: bool = False
    error: str = None

   #making sending a jsonified dictionary
    def drop():
        pass


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
@app.route('/keyval/<string:key>', methods=['POST', 'PUT'])
def keyv_insert():
    #json value returns
    jsons = JsonResponse(command='CREATE' if request_method=='POST' else'UPDATE')

    #checking the redis payloads
    try:
        payloads = request.get_json()
        json_key = payload['key']
        json_value = payload['value']
        json_command += f' {payload['key']}/{payload['value']}
    except:
        json_error = "Error in Json clients"
        return jsonify(jsons), 400

    #Connecting to Redis
    try:
        test_val = redis.get(json_key)
    except:
        json_error = "Unable to connect to Redis."
        return jsonify(jsons), 400
    
    #Creating Redis~~~~POST
    if request_method == 'POST' and not test_val == None:
        json_error = "Unable to create new keyvals because its already made"
        return jsonify(jsons), 409

    #Creating Redis~~~~PUT
    elif request_method =='PUT' and test_val == None:
        json_error = "Unable to Update keyvals"
        return jsonify(jsons), 404

    #Creating/Updating the record keyvals
    else:
        if redis.set(json_key, json_value) == False:
            json_error = "Error creating keyval records"
            return jsonify(jsons), 400
        else:
            json_resuls = True
            return jsonify(jsons), 200

@app.route('/keyval/<string:key>', methods=['GET', 'DELETE'])
def keyv_return(key):
    ret_json ={ 
        'key': key,
        'value':  None,
        'command': None,
        'result': False,
        'error':  None
    }

    #Checking Redis connections
    try:
        test_val = redis.get(key)
    except RedisError:
        ret_json['error'] = " Failed to connect to Redis"
        return jsonify(ret_json), 400

    #Unable to retrieve/deleting the non-existing keyvals
    if test_val==None:
        ret_json['error'] = "key is non existant"
        return jsonify(ret_json)
    #else:
       # ret_json['value'] = test_val.decode

    #Retrieving Redis~~~~GET
    if request_method == 'GET':
        ret_json['result'] = True
        return jsonify(ret_json), 200

    #Removing Redis~~~~DELETE
    elif request_method == 'DELETE':
        returning = redis_delete(key)
        if returning == 1:
            ret_json['result'] = True
            return jsonify(ret_json)
        else:
            ret_json['error'] = "Failed to DELETE keyvalue"
            return jsonify(ret_json), 400
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
