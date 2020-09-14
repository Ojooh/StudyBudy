import os, json, datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from notes.utils.determine_state import DetermineState
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm
from users.models import UserState
from notes.models import FileSystem
from quiz.models import QuizFileSystem
from studybudy.settings import BASE_DIR


media_root = settings.MEDIA_ROOT
Users = get_user_model()

# Create your views here.
@login_required(login_url='/login')
def profile(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        full_name       = request.user.get_full_name()
        profile_pic     = request.user.profile_photo
        dob             = request.user.dob
        utype            = request.user.user_type
        cs              = request.user.get_country_state()
        school          = request.user.school
        email           = request.user.email
        telephone       = request.user.telephone 
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        mode            = DS.determine_mode()
        file_count      = FileSystem.objects.filter(owner=request.user, file_type="file", active=True).count()
        folder_count    = FileSystem.objects.filter(owner=request.user, file_type="folder", active=True).count()
        quiz_count      = QuizFileSystem.objects.filter(owner=request.user, file_type="quiz_file", active=True).count()
        trash_count     = FileSystem.objects.filter(owner=request.user, file_type="file", active=False).count()
        path            = "user/" + mode + "/profile.html"

        context = {
            'short_name'    : sname,
            'full_name'     : full_name,
            'profile_pic'   : profile_pic,
            'dob'           : dob,
            'role'          : utype,
            'cs'            : cs,
            'school'        : school,
            'email'         : email,
            'telephone'     : telephone,
            'file_count'    : file_count,
            'folder_count'  : folder_count,
            'quiz_count'    : quiz_count,
            'trash_count'   : trash_count,
            'user'          : request.user
        }
    else:
        return redirect("/login")

    return render(request, path, context)


@login_required(login_url='/login')
def change_password(request):
    if (request.user.is_authenticated):
        return render(request, "auth/change_password.html")
    else:
        return redirect("/login")


@login_required(login_url='/login')
def edit_profile(request, user_id):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        mode            = DS.determine_mode()
        user_inst       = get_object_or_404(Users, pk=user_id)
        orig_pass       = user_inst.password
        form            = ProfileForm(instance=user_inst)
        path            = "user/" + mode + "/editProfile.html"
        # user_i       = get_object_or_404(Users, pk=3)
        # user_i.set_password("password4")
        # user_i.save()


        if request.method == "POST" : 
            form = ProfileForm(request.POST, request.FILES, instance=user_inst)
            # print(form.cleaned_data.get("country"))
            if form.is_valid():
                user = form.save()
                if form.cleaned_data.get("password") == "":
                    user.password = orig_pass
                else:
                    user.set_password(form.cleaned_data.get("password"))
                user.last_editted = datetime.now()
                user.save()

                return redirect('/User/profile/')

        context = {
            'short_name'    : sname,
            'user'          : request.user,
            'form'          : form
        }
    else:
        return redirect("/login")

    return render(request, path, context)


@login_required(login_url='/login')
def delete_image(request, user_id):
    sname = None
    if (request.user.is_authenticated):
        user_inst       = get_object_or_404(Users, pk=user_id)
        user_inst.profile_photo.delete(save=True)
        path            = "/User/" + user_id + "/edit_profile/"
        

    else:
        return redirect("/login")

    return redirect(path)



@login_required(login_url='/login')
def change(request):
    old = request.GET.get('old')
    new = request.GET.get('new')
    data = {}

    if (request.user.is_authenticated):
        user        = get_object_or_404(Users, pk=request.user.id)
        user_old    = user.password

        if old == "" or new =="":
            data['error'] = "Invalid Password entered must be a charcter"
        elif len(new) <= 6:
            data['error'] = "Invalid New Password is not long enough"
        else:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user) 
            data["url"] = "/Dashboard"
        

    else:
        return redirect("/login")


           
    return JsonResponse(data)


