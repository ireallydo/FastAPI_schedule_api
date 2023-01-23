import requests
import json

#!TODO: more elegant with all those 0 and 1 in lists and null values
#!TODO: working with responses

def check_for_code_200(func_name, response, response_model, list=False):
    if response.status_code == 200:
        print(func_name + ': OK')
        if response_model == False:
            response_out = response.text
        elif list == False:
            response_out: response_model = response_model(**(json.loads(response.text)))
        else:
            response_out =  response_model(__root__=(json.loads(response.text)))
    else:
        print(func_name + ': sth went wrong')
        print(response.status_code)
        print(response)
        print(response.text)
        response_out = response.text
    return response_out

def check_for_code_201(func_name, response, response_model=False):
        if response.status_code == 201:
            print(func_name + ': OK')
            if response_model != False:
                response_out: response_model = response_model(**(json.loads(response.text)))
            else:
                response_out = response.text
        else:
            print(func_name + ': sth went wrong')
            print(response.status_code)
            print(response)
            print(response.text)
            response_out = response.text
        return response_out

def check_for_code_204(func_name, response):
    if response.status_code == 204:
        print(func_name + ': OK')
    else:
        print(func_name + ': sth went wrong')
        print(response.status_code)
        print(response)
        print(response.text)
    response_out = response.text
    return response_out

def check_for_code_401(func_name, response):
    if response.status_code == 401:
        print(func_name + ': OK')
    else:
        print(func_name + ': sth went wrong')
        print(response.status_code)
        print(response)
        print(response.text)
    response_out = response.text
    return response_out

def check_for_code_403(func_name, response):
    if response.status_code == 403:
        print(func_name + ': OK')
    else:
        print(func_name + ': sth went wrong')
        print(response.status_code)
        print(response)
        print(response.text)
    response_out = response.text
    return response_out

def check_for_code_404(func_name, response):
    if response.status_code == 404:
        print(func_name + ': OK')
    else:
        print(func_name + ': sth went wrong')
        print(response.status_code)
        print(response)
        print(response.text)
    response_out = response.text
    return response_out
