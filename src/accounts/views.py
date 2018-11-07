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
        token = request.POST.get('id_token')
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
