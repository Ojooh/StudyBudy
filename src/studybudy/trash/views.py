import json, os
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from notes.utils.determine_state import DetermineState
from users.models import UserState
from notes.models import FileSystem
from quiz.models import QuizFileSystem

Users = get_user_model()

# Create your views here.
@login_required(login_url='/login')
def trash(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        note_folders    = FileSystem.objects.filter(active=False, owner=request.user.id, file_type="folder").order_by(fryp)
        quiz_folders    = QuizFileSystem.objects.filter(active=False, owner=request.user.id, file_type="quiz_folder").order_by(fryp)
        note_files      = FileSystem.objects.filter(active=False, owner=request.user.id, file_type="file",).order_by(fry)
        quiz_files      = QuizFileSystem.objects.filter(active=False, owner=request.user.id, file_type="quiz_file").order_by(fryp)
        path            = "trash/" + mode + "/trash.html"

        context = {
            'short_name': sname,
            'folders'   : list(note_folders) + list(quiz_folders),
            'files'     : list(note_files) + list(quiz_files),
            'state'     : state,
            'filt'      : filt,
            'folt'      : folt,
        }
        return render(request, path, context)
    else:
        return redirect("/login")


@login_required(login_url='/login')
def recycle_list(request):
    pk              = request.GET.get('ID')
    file_typey      = request.GET.get('typey')
    data            = {}
    x               = []

    if (request.user.is_authenticated):
        if file_typey == "quiz_file" or file_typey == "quiz_folder":
            qs      = QuizFileSystem.objects.filter(Q(pk=int(pk), owner=request.user, active=False,) | Q(folder=int(pk), owner=request.user, active=False))
        else:
            qs      = FileSystem.objects.filter(Q(pk=int(pk), owner=request.user, active=False,) | Q(folder=int(pk), owner=request.user, active=False))

        if qs is None:
            data["error"] = "Something Went Wrong, File does not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        else:
            for b in qs:
                y = {}
                y["f_id"]   = b.id
                y["f_name"] = b.name
                y["f_size"] = b.size
                y["f_type"] = b.file_type
                x.append(y)
                
            data["src"] = x
            print(x)
            return JsonResponse(data)
        
    else:
        return redirect("/login")



@login_required(login_url='/login')
def recycle(request):
    pk              = request.GET.get('ID')
    file_typey      = request.GET.get('typey')
    data            = {}
    loop_list       = []

    if (request.user.is_authenticated):
        if file_typey == "quiz_file" or file_typey == "quiz_folder":
            q1      = QuizFileSystem.objects.filter(Q(pk=int(pk), owner=request.user, active=False,) | Q(folder=int(pk), owner=request.user, active=False))
        else:
            q1      = FileSystem.objects.filter(Q(pk=int(pk), owner=request.user, active=False,) | Q(folder=int(pk), owner=request.user, active=False))

        if q1 is None:
            data["error"] = "Something Went Wrong, File does not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        else:
            loop_list.append(q1)
            while len(loop_list) != 0:
                for res in loop_list[0]:
                    if res.owner == request.user:
                        if res.file_type == "folder":
                            fold = res.folder
                            retz = res.size
                            res.active = True
                            res.sharable    = False
                            res.shared_with = ""
                            res.save()

                            # sub_sub_file = FileSystem.objects.filter(folder=int(res.id))
                            # loop_list.append(sub_sub_file)
                            if fold != 0:
                                yl = FileSystem.objects.get(pk=int(fold))
                                if yl.active :
                                    pass
                                else:
                                    res.folder = 0
                                    res.save()
                        
                        if res.file_type == "quiz_folder":
                            fold = res.folder
                            retz = res.size
                            res.active = True
                            res.sharable    = False
                            res.shared_with = ""
                            res.save()

                            # sub_sub_file = FileSystem.objects.filter(folder=int(res.id))
                            # loop_list.append(sub_sub_file)
                            if fold != 0:
                                yl = FileSystem.objects.get(pk=int(fold))
                                if yl.active :
                                    pass
                                else:
                                    res.folder = 0
                                    res.save()

                        if res.file_type == "file":
                            fold = res.folder
                            retz = res.size
                            res.active = True
                            res.sharable    = False
                            res.shared_with = ""
                            res.save()

                            while fold != 0:
                                yl = FileSystem.objects.get(pk=int(fold))
                                fold = yl.folder
                                if yl.active :
                                    ret = yl.size
                                    if ret != retz:
                                        ter = ret + retz
                                        yl.size = ter
                                        yl.save()
                                    else:
                                        pass
                                else:
                                    ret = yl.size
                                    ter = ret - retz
                                    yl.size = ter
                                    yl.save()
                                    res.folder = 0
                                    res.save()

                        if res.file_type == "quiz_file":
                            fold = res.folder
                            retz = res.size
                            res.active = True
                            res.sharable    = False
                            res.shared_with = ""
                            res.save()

                            while fold != 0:
                                yl = QuizFileSystem.objects.get(pk=int(fold))
                                fold = yl.folder
                                if yl.active :
                                    ret = yl.size
                                    if ret != retz:
                                        ter = ret + retz
                                        yl.size = ter
                                        yl.save()
                                    else:
                                        pass
                                else:
                                    ret = yl.size
                                    ter = ret - retz
                                    yl.size = ter
                                    yl.save()
                                    res.folder = 0
                                    res.save()
                
                loop_list.pop(0)

            data["success"] = "Operation Successful, File(s) have been restored"
            return JsonResponse(data)

    return JsonResponse(data)


@login_required(login_url="/login")
def get_details(request):
    pk          = request.GET.get('ID')
    file_typey  = request.GET.get('typey')
    data = {}

    if (request.user.is_authenticated):  
        if file_typey == "quiz_file" or file_typey == "quiz_folder":
            qs      = QuizFileSystem.objects.get(pk=int(pk))
        else:
            qs      = FileSystem.objects.get(pk=int(pk))

        
        if qs is None:
            data["error"] = "Something Went Wrong, Please Try Again"
            return JsonResponse(data)
        else:
            data['id']          = str(pk)
            data['file_name']   = str(qs.name)
            data['size']        = str(qs.size)
            data['location']    = str(qs.location)
            data['created']     = qs.date_created.strftime("%H:%M:%S - %b %d %Y")

            if file_typey != "quiz_file" and file_typey != "quiz_folder":
                if qs.description == None:
                    data['description'] = ""
                else:
                    data['description'] = str(qs.description)
            else:
                data['description'] = ""
            if qs.file_type == "file":
                data['file_type']   = "PDF file"
            elif qs.file_type == "quiz_file":
                data['file_type']   = "JSON file"
            else:
                data['file_type']   = str(qs.file_type)
            if qs.owner == request.user:
                data['owner'] = "Me"
            else:
                data['owner'] = str(qs.owner)
            if qs.last_editted_by == request.user:
                data['editted_by'] = "Me"
            else:
                data['editted_by'] = str(qs.last_editted_by)
            if qs.last_editted == None:
                data['last_modified']   = "never"
            else:
                data['last_modified']   = qs.last_editted.strftime("%H:%M:%S - %b %d %Y")
            if qs.last_opened == None:
                data['last_opened']     = "never"
            else:
                data['last_opened']     = qs.last_opened.strftime("%H:%M:%S - %b %d %Y")
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url='/login')
def delete_permanently(request):
    data = {}
    active_id   = request.GET.get('file_id')
    file_typey  = request.GET.get('typey')

    if (request.user.is_authenticated):
        user_state  = UserState.objects.get(user=request.user)
        if file_typey == "quiz_file" or file_typey == "quiz_folder":
            qs      = QuizFileSystem.objects.get(pk=int(active_id))
        else:
            qs      = FileSystem.objects.get(pk=int(active_id))


        if qs is None:
            data['msg'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        else:
            prev_size                   = user_state.total_storage
            user_state.total_storage    = prev_size -  qs.size
            user_state.save()
            qs.location.delete(save=True)
            qs.delete()
            if file_typey == "quiz_file" or file_typey == "quiz_folder":
                data['msg'] = "Quiz File has been Deleted Permanently"
            else:
                data['msg'] = qs.file_type.capitalize() + " has been Deleted Permanently"
    else:
        return redirect("/login")
        
    return JsonResponse(data)

    
