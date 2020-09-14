from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .utils.validate import DataValidator
from users.models import UserState

User = get_user_model()


def login_page(request):
    return render(request, "auth/login.html")


def register_page(request):
    return render(request, "auth/register.html")


def login_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    data = {}

    user = authenticate(request, username=username, password=password)
    if user is not None and user.active:
        login(request, user)

        if ((request.user.is_staff and request.user.is_admin) and (request.user.user_type == "Admin IT")):
             data['url'] = "/admin"
        elif request.user.is_staff and request.user.user_type == "Admin Editor":
            data['url'] = "/admin"
        else:
            data['url'] = "/Dashboard"
    else:
        data['error'] = "Invalid Username and Password"

        
    
    return JsonResponse(data)


def register_user(request):
    user_category       = request.GET.get('user_category').capitalize()
    fname               = request.GET.get('fname').capitalize()
    lname               = request.GET.get('lname').capitalize()
    dob_day             = request.GET.get('dob_day')
    dob_mnth            = request.GET.get('dob_mnth')
    dob_year            = request.GET.get('dob_year') 
    sex                 = request.GET.get('sex').capitalize()
    ctry                = request.GET.get('ctry').capitalize() 
    state               = request.GET.get('state').capitalize()
    tos                 = request.GET.get('tos').capitalize() 
    class_study         = request.GET.get('class_study').capitalize()
    school              = request.GET.get('school').capitalize() 
    email               = request.GET.get('email') 
    tel                 = request.GET.get('tel')
    facebook            = request.GET.get('facebook') 
    twitter             = request.GET.get('twitter')
    IG                  = request.GET.get('IG')
    data                = {}
    dv                  = DataValidator()

    empt_arr = [user_category, fname, lname, dob_day, dob_mnth, dob_year, sex, ctry, state, tos, class_study, email]

    empty = dv.is_empty(empt_arr)

    if empty == False:
        datey = dv.date_format([dob_day, dob_mnth, dob_year])
        railey = dv.email_unique(email)
        tailey = dv.telephone_unique(tel)

        if school != "":
            namey = dv.nameRegex([fname, lname, sex, ctry, state, tos, class_study, school])
            if tel != "":
                teley = dv.teleRegex([tel])
            else:
                teley = True
        else:
            namey = True


        if namey and teley and railey:
            new_user            = User.objects.create_user(email, fname, lname, sex, datey, user_category, "password4")
            new_user.country    = ctry
            new_user.state      = state
            new_user.los        = tos
            new_user.los_class  = class_study
            new_user.school     = school
            new_user.telephone  = tel
            new_user.facebook   = facebook
            new_user.twitter    = twitter
            new_user.instagram  = IG
            new_user.shared_with_me = "[]"
            new_user.save()
            us = UserState()
            us.user = new_user
            us.save()

            if new_user is not None:
                # login(request, new_user)

                # if request.user.is_staff and request.user.is_admin:
                #     data['url'] = "/admin"
                # else:
                data['url'] = "/login"
            else:
                data['error'] = "Invalid Data Input"
        else:
            if railey == False:
                data["error"] = "Email already has been taken"
            elif tailey == False:
                data["error"] = "Telephone number already has been taken"
            else:
                data['error'] = "Invalid Username and Password"
 
    return JsonResponse(data)


def logout_user(request):
    logout(request)
    return redirect("/login") 