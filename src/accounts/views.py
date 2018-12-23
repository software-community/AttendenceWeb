from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Google AUTH
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


# Create your views here.
@csrf_exempt
def tokenAuth(request):

    if request.method == 'POST':
        # print(request.META['HTTP_AUTHORIZATION'])
        token = request.META['HTTP_AUTHORIZATION']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        # display_name = user.displayName.split(" ")
        django_user, created = User.objects.get_or_create(email = user.email, defaults = {
            'username': uid,
            'password': 'iitropar',
            # 'first_name': display_name[0],
            # 'last_name': display_name[1]
        })
        print(user.email)
        
    return HttpResponse("Sucess")

@csrf_exempt
def login(request):
     if request.method == 'POST':
        # print(request.META['HTTP_AUTHORIZATION'])
        token = request.META['HTTP_AUTHORIZATION']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        display_name = user.displayName.split(" ")
        django_user, created = User.objects.get_or_create(email = user.email, defaults = {
            'username': uid,
            'password': 'iitropar',
            'first_name': display_name[0],
            'last_name': display_name[1]
        })
        return HttpResponse({"profile_id": user.profile.id})

