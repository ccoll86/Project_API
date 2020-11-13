#--------------CLI--------------#
import requests
import sys
import argparse
import textwrap

HOST = "34.121.122.205"

parser = argparse.ArgumentParser( 
    formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''
                              ~ Group 1 Tool Commands ~
			       -----------------------
        Choose one of the following! If you need help please type -> python3 cli.py -h

			       md5 - use: md5 -> string
			   factorial - use: factorial -> num
			   fibonacci - use: fibonacci -> num
			      prime - use: is-prime -> num
			kyeval - use: keyval-Redis_options -> string'''))
			
parser.print_help()

subparsers = parser.add_subparsers(help='commands', dest='cli')

#Creating all parsers for the API functions
#md5
md5_parser = subparsers.add_parser('md5', help='Displays a string as a json value hex')
md5_parser.add_argument('md5_string', help='Displays a string as a json value hex',action='store')

#factorial
fact_parser = subparsers.add_parser('factorial', help=' an integer as a factorial')
fact_parser.add_argument('fact_integer', help='Returns an integer as a factorial', action='store')

#fibonacci
fib_parser = subparsers.add_parser('fibonacci', help='Returns fibbonacci value')
fib_parser.add_argument('fib_integer', help='Returns fibbonacci value', action='store')

#is-prime
prime_parser = subparsers.add_parser('prime', help='Returns a true or false')
prime_parser.add_argument('prime_integer', help='Returns a true or false', action='store')

#keyval 
keyval_parser = subparsers.add_parser('keyval', help='Use this to control the Redis Keyvals. Enter a key value then chose an option: -post, -get, -put, -delete')
keyval_parser.add_argument('keyval_parser', action='store', help='The Keyval thing')
keyval_parser.add_argument('-post', help='This writes a new key-value pair')
keyval_parser.add_argument('-get', help='This to retrieve the value')
keyval_parser.add_argument('-put', help='This overwrite the value on an existing key')
keyval_parser.add_argument('-delete', help='Use to delete key (and value) supplied')


args = parser.parse_args()
def md5():
    if args.cli == 'md5':
        input_md5string = args.md5_string
        md5=requests.get(HOST + input_md5string)
        print(md5.text)

def factorial():
    if args.cli == 'factorial':
        input_factint = args.fact_int
        factorial=requests.get(HOST + input_factint)
        print(factorial.text)
	
def fibonacci():
    if args.cli == 'fibonacci':
        input_fibint = args.fib_int
        fibonacci=requests.get(HOST + input_fibint)
        print(fibonacci.text)

def prime():
    if args.cli == 'prime':
        input_primeint = args.prime_int
        prime=requests.get(HOST+input_primeint)
        print(prime.text)

def keyval():
    if args.cli == 'keyval':
        if args.cli == '-post':
            input_keystr = args.keyval_parser
            r=requests.get(HOST + input_keystr)
            print(r.text)
        if args.cli == '-get':
            input_keystr = args.keyval_parser
            r=requests.get(HOST + input_keystr)
        if args.cli == 'put':
            input_keystr = args.keyval_parser
            r=requests.get(HOST + input_keystr)
        if args.cli == '-delete':
            input_keystr = args.keyval_parser
            r=requests.get(HOST + input_keystr)
        else:
            print('Specify the Redis command you want to use')

