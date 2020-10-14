from flask import Flask,jsonify, Response
import math
import hashlib

#instantiate the Flask object
app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome to the Project 5 API"

# md5 hash converter
@app.route('/md5/<string:input>', methods=['GET'])
def get_md5(input):
	res = hashlib.md5(input.encode())
	return jsonify(
        f'input:{input}',
        {'Hash': str(res.hexdigest())}
    )


# Factorial endpoint
@app.route('/factorial/')
def factorial(resl = 'reslult'):
    num = int(input('Input a number to complete factorial: '))
    resl = math.factorial(num)
    return jsonify(
        f'Input: {num}', 
        f'Output: {resl}'

    )

# Fibonacci endpoint
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

        return jsonify(
            f"Input: {n}",
            f"Output: {array}"
        )

#  prime check endpoint
@app.route('/is-prime/<int:n>')
def prime_check(n):
    if n > 1: 
        for i in range(2, n):
            if (n % i) == 0:
                x = "False"
                break
                
        else:
            x = "True"

        return jsonify(
            f"{x}"
            )

@app.route('/slack-alert/<string:x>')
def slack_alert(x):
    from slackclient import SlackClient

    slack_token = os.environ['xoxb-73266387591-1450694768528-LCKQlzoPkr1ueW2gkfyyW2t3']
    sc = SlackClient(slack_token)

    sc.api_call(
        "chat.postMessage",
        channel="#group1",
        text="Hello from Python! :tada:"
)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
