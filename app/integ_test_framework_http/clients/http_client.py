import requests
import json

def post(session, url, payload, headers):
    response = session.post(url, data=payload, headers=headers)
    return response

def post_file(session, url, payload, headers):
    response = session.post(url, files=payload, headers=headers)
    return response

def get(session, url, payload, headers):
    response = session.get(url, data=payload, headers=headers)
    return response

def patch(session, url, payload, headers):
    response = session.patch(url, data=payload, headers=headers)
    return response

def delete(session, url, payload, headers):
    response = session.delete(url, data=payload, headers=headers)
    return response
