from django.shortcuts import render
from django.http import HttpResponse

# Google AUTH
from google.oauth2 import id_token
from google.auth.transport import requests

# Create your views here.

def tokenAuth(request):
    # print(request)
    CLIENT_ID = "386503521006-c75b5olnj3rq7pei87gjgjnn68kviuu5.apps.googleusercontent.com"
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk4Njk0NWJmMWIwNDYxZjBiZDViNTRhZWQ0YzQ1ZWU0ODMzMjgxOWEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY29sbGVhZ3VlLXNvZmNvbSIsIm5hbWUiOiJLYXJhbiBTZWhnYWwiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1EaTFKNW5fcDdjWS9BQUFBQUFBQUFBSS9BQUFBQUFBQU16MC9tWHdKa0EwR2R5RS9zOTYtYy9waG90by5qcGciLCJhdWQiOiJjb2xsZWFndWUtc29mY29tIiwiYXV0aF90aW1lIjoxNTQxMjQwMDEzLCJ1c2VyX2lkIjoiTWRTVTBKWWxpR1k1cWRHOWhXWXpTakNOc3BKMiIsInN1YiI6Ik1kU1UwSllsaUdZNXFkRzloV1l6U2pDTnNwSjIiLCJpYXQiOjE1NDEyNDAwMTMsImV4cCI6MTU0MTI0MzYxMywiZW1haWwiOiJrYXJhbi5zaGdsOTZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTI4ODM1Njg5MzQxODcxMjg3NDkiXSwiZW1haWwiOlsia2FyYW4uc2hnbDk2QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.roIS_lPmUDSMlxArdlzW6QcPzv3keI2LjakSVU8aHvRQZYEfRTcT8CH9aK5vx9jbIApIEFqYqPVR7x658dq8sjPgt0yc4D8lHKQ9GjQIlcPPp_Zxl1w6FjKVwNwzHIFcQak-YZqTW4kvTK6Imwd0VZJCO4F7kjDCcXj2BfSDVQ_klovubey5oJ0HMk9COGhQBcQR9Zm9"
    # try:
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    userid = idinfo['sub']
    print(userid)
    # except ValueError:
    #     # Invalid token
    #     print("INVALID TOKEN")
    #     pass

    return HttpResponse("Sucess")
