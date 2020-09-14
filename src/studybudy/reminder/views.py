import os, json, time, pytz
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from notes.utils.determine_state import DetermineState
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from users.models import UserState
from notes.models import FileSystem
from quiz.models import QuizFileSystem
from .models import TaskReminder
from .forms import TaskForm
from .tasks import send_email_reminder
from django.utils.timezone import make_aware
from users.models import Notifications
from studybudy.settings import BASE_DIR




media_root  = settings.MEDIA_ROOT
Users       = get_user_model()
utc         = pytz.UTC


# Create your views here.
@login_required(login_url='/login')
def task_list(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        task_list       = TaskReminder.objects.filter(passed=False, user=request.user.id).order_by('created')
        for x in task_list:
            if utc.localize(datetime.now()) > x.time:
                notyss  = Notifications.objects.filter(task_id=x.id).first()
                if notyss is not None:
                    notyss.delete()
                x.delete()

        path            = "reminder/" + mode + "/taskList.html"

        context = {
            'short_name': sname,
            'task_list' : task_list,
        }
    else:
        return redirect("/login")

    return render(request, path, context)


@login_required(login_url='/login')
def add_task(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        form            = TaskForm(request.POST or None)

        if request.method == "POST": 
            form = TaskForm(request.POST)
            if form.is_valid(): 
                task                = form.cleaned_data.get("task").capitalize()
                date_scheduled      = form.cleaned_data.get("date_scheduled")
                time                = form.cleaned_data.get("time")
                timezone            = time.tzname
                data_S              = date_scheduled.strftime('%Y-%m-%d')
                time_S              = time.strftime('%H:%M:%S')
                join_datetime       = data_S + " " + time_S
                date_set            = datetime.strptime(join_datetime, "%Y-%m-%d %H:%M:%S")

                new_task                = TaskReminder()
                new_task.user           = request.user
                new_task.phone_number   = request.user.telephone
                new_task.task           = task
                new_task.time           = make_aware(date_set)
                new_task.save()

                

                if new_task is not None:
                    # send_email_reminder.apply_async(args=(new_task.id,"davidmatthew708@gmail.com"), eta=new_task.time)
                    new_note                = Notifications()
                    new_note.usey           = request.user
                    new_note.task_id        = new_task.id
                    new_note.notify         = task + " reminder has been created"
                    new_note.save()
                    
                return redirect('/Reminder/')

        context = {
            'short_name'    : sname,
            'user'          : request.user,
            'form'          : form,
        }
    else:
        return redirect("/login")

    return render(request, "reminder/Light-mode/addTask.html", context)


@login_required(login_url='/login')
def edit_task(request, task_id):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        task_inst       = get_object_or_404(TaskReminder, pk=task_id)
        form            = TaskForm(request.POST or None)
        text_task       = task_inst.task
        date_scheduled  = task_inst.time.strftime('%Y-%m-%d')
        time            = task_inst.time.strftime('%H:%M:%S')


        if request.method == "POST": 
            form = TaskForm(request.POST)
            
            if form.is_valid():
                task                = form.cleaned_data.get("task").capitalize()
                date_scheduled      = form.cleaned_data.get("date_scheduled")
                time                = form.cleaned_data.get("time")
                timezone            = time.tzname
                data_S              = date_scheduled.strftime('%Y-%m-%d')
                time_S              = time.strftime('%H:%M:%S')
                join_datetime       = data_S + " " + time_S
                date_set            = datetime.strptime(join_datetime, "%Y-%m-%d %H:%M:%S")

                task_inst.user           = request.user
                task_inst.phone_number   = request.user.telephone
                task_inst.task           = task
                task_inst.time           = make_aware(date_set)
                task_inst.save()
                
                if task_inst is not None:
                    # send_email_reminder.apply_async(args=(new_task.id,"davidmatthew708@gmail.com"), eta=new_task.time)
                    new_note                = Notifications.objects.filter(task_id=task_inst.id).first()
                    new_note.usey           = request.user
                    new_note.task_id        = task_inst.id
                    new_note.notify         = task_inst.task + " reminder has been created"
                    new_note.save()
                
               

                return redirect('/Reminder/')

        context = {
            'short_name'    : sname,
            'user'          : request.user,
            'form'          : form,
            'task'          : text_task,
            'date_scheduled': date_scheduled,
            'time'          : time,
        }
    else:
        return redirect("/login")

    return render(request, "reminder/Light-mode/addTask.html", context)


@login_required(login_url='/login')
def delete_task(request):
    data = {}
    task_id   = request.GET.get('ID')

    if (request.user.is_authenticated):
        active_task = TaskReminder.objects.get(pk=int(task_id))

        if active_task is None:
            data['error'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)

        else:
            active_task.delete()
            noty = Notifications.objects.filter(task_id=int(task_id)).first()
            noty.delete()
            data["success"] = "Task successfully deleted"

    else:
        return redirect("/login")
        

    return JsonResponse(data)

            
@login_required(login_url='/login')
def complete_task(request):
    data = {}
    task_id         = request.GET.get('ID')
    task_status     = request.GET.get('status')

    if (request.user.is_authenticated):
        active_task = TaskReminder.objects.get(pk=int(task_id))

        if active_task is None:
            data['error'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)

        else:
            if task_status == "True":
                active_task.completed = True
            else:
                active_task.completed = False
            active_task.save()
            noty = Notifications.objects.filter(task_id=int(task_id)).first()
            noty.delete()
            data["success"] = "Task has successfully been completed"

    else:
        return redirect("/login")
        

    return JsonResponse(data)

                    
               

          






