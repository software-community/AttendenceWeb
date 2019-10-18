from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

# Google AUTH
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from accounts.models import Teacher, Student, Profile


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
        django_user, created = User.objects.get_or_create(email=user.email, defaults={
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
        try:
            token = request.META['HTTP_AUTHORIZATION']
            data = request.body.decode('utf-8')
            data = json.loads(data)
            is_student = data.get('is_student')
            is_teacher = data.get('is_teacher')

            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            django_user, _ = User.objects.get_or_create(
                email=user.email, username=user.uid)

            profile, created = Profile.objects.get_or_create(
                user=django_user, is_student=is_student, is_teacher=is_teacher)

            _id = None
            if(is_student):
                _id = Student.objects.get(student=profile).id
            elif(is_teacher):
                _id = Teacher.objects.get(teacher=profile).id

            return JsonResponse({'status': 'ok', "_id": _id, "is_student": profile.is_student, "is_teacher": profile.is_teacher})
        except Exception as err:
            print(err)
            return JsonResponse({'status': 'error'})
