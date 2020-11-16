import requests

HOST = "http://34.121.122.205:5000"


#----------------Here is the new script---------------------

#Calculated final testing
errors= 0
successful_tests= 0
all_tests = 19

#Keyval tests
print("Beginning Keyval Tests!")

#GET
def keyvalGET():
    total = {'/keyval/test1':'test1'}
    for path, result in total.items():
        keyvalGET=requests.get(f'http://{HOST}{path}')
        if keyvalGET.status_code == 200:
            value = keyvalGET.json()['key']
            if value == result
                successful_tests +=1
                print("Success, keyval GET is correct!")
            else:
                error +=1
                print("Unsuccessful, keyval GET is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(keyvalGET.status_code))

#POST           
def keyvalPOST():
    jeep = 'jeep2'
    escape = 'escape'
    data = {'key':jeep, 'value':escape} 
    keyvalPOST=requests.post(f'http://{HOST}/keyval',json=data) 
    if keyvalPOST.status_code == 200:
        value = keyvalPOST.json()['key']
        if value == jeep:
            successful_tests +=1
            print("Success, keyval POST is correct!")
        else:
            error +=1
            print("Unsuccessful, keyval POST is wrong") 
    else:
        error +=1
        print("Unsuccessful, this is the response code ", str(keyvalPOST.status_code))

#DELETE
def keyvalDELETE():
    jeep = 'jeep2'
    escape = 'escape3'
    keyvalDELETE=requests.delete(f'http://{HOST}/keyval/jeep2') 
        if keyvalDELETE.status_code == 200:
            value = keyvalDELETE.json()['result']
            if value == True:
                successful_tests +=1
                print("Success, keyval DELETE is correct!")
            else:
                error +=1
                print("Unsuccessful, keyval DELETE is wrong") 
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(keyvalDELETE.status_code)) 

#PUT
def keyvalPUT():
    jeep = 'jeep2'
    escape = 'escape3'
    data = {'key':jeep, 'value':escape}  
    keyvalPUT=requests.put(f'http://{HOST}/keyval', json=data) 
        if keyvalPOST.status_code == 200:
            value = keyvalPUT.json()['value']
            if value == escape:
                successful_tests +=1
                print("Success, keyval PUT is correct!")
            else:
                error +=1
                print("Unsuccessful, keyval PUT is wrong") 
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(keyvalPUT.status_code))


#md5 testing
print("Beginning md5 Test!")
def md5():
    total = {'/md5/test': '098f6bcd4621d373cade4e832627b4f6', '/md5/testtesttest': '1fb0e331c05a52d5eb847d6fc018320d', '/md5/tester': 'f5d1278e8109edd94e1e4197e04873b9'}
    for path, result in total.items():
        md5=requests.get(f'http://{HOST}{path}')
        if md5.status_code == 200:
            value=md5.json()['output']
            if value == result:
                successful_tests +=1
                print("Success, md5 is correct!")
            else:
                error +=1
                print("Unsuccessful, md5 is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(md5.status_code))


#Is-Prime testing
print("Beginnning Prime Tests!")
def prime():
    total = {'/is-prime/8': 'False', '/is-prime/2': 'True', '/is-prime/6': 'False'}
    for path, result in total.items():
        prime =requests.get(f'http://{HOST}{path}')
        if prime.status_code == 200:
            value=prime.json()['output']
            if value == result:
                successful_tests +=1
                print("Success, is-prime is correct!")
            else:
                error +=1
                print("Unsuccessful, is-prime is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(prime.status_code))


#Factorial testing
print("Beginning Factorial Test!")
def factorial():
    total = {'/factorial/4': 24, '/factorial/5': 120, '/factorial/9': 362880}
    for path, result in total.items():
        factorial=requests.get(f'http://{HOST}{path}')
        if factorial.status_code == 200:
            value=factorial.json()['output']
            if value == result:
                successful_tests +=1
                print("Success, factorial is correct!")
            else:
                error +=1
                print("Unsuccessful, factorial is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(factorial.status_code))


#Fibonacci testing
print("Beginning Fibonacci Test!")
def fibonacci():
    total = {'/fibonacci/10': '[0,1,1,2,3,5,8]', '/fibonacci/18': '[0,1,1,2,3,5,8,13]', '/fibonacci/56': '[0,1,1,2,3,5,8,13,21,34,55]'}
    for path, result in total.items():
        fibonacci=requests.get(f'http://{HOST}{path}')
        if fibonacci.status_code == 200:
            value=fibonacci.json()['output']
            if value == result:
                successful_tests +=1
                print("Success, fibonacci is correct!")
            else:
                error +=1
                print("Unsuccessful, fibonacci is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(fibonacci.status_code))


#Slack testing
print("Beginning Slack Test!")
def slackalert():
    total = {'/slack-alert/testing': 'Message sent and posted successfully to Slack channel', '/slack-alert/Hello%20World': 'Message sent and posted successfully to Slack channel', '/slack-alert/This%20Is%20A%20Big%20String.': 'Message sent and posted successfully to Slack channel'}
    for path, result in total.items():
        slackalert=requests.get(f'http://{HOST}{path}')
        if slackalert.status_code == 200:
            value=slackalert.json()['message']
            if value == result:
                successful_tests +=1
                print("Success, slack-alert is correct!")
            else:
                error +=1
                print("Unsuccessful, slack-alert is wrong")
        else:
            error +=1
            print("Unsuccessful, this is the response code ", str(slackalert.status_code))



#Calculating final scores
print("Errors found: ", str(errors), "Successful tests: ", str(successful_tests), "out of ", str(all_tests))
print("Total grade is: ", str((successful_tests / all_tests)*100), "%" )
