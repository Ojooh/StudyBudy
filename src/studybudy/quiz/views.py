import os, json
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from notes.utils.determine_state import DetermineState
from notes.utils.remove_share import RemoveShare
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from users.models import UserState
from notes.models import FileSystem
from .models import QuizFileSystem
from studybudy.settings import BASE_DIR


media_root = settings.MEDIA_ROOT
Users = get_user_model()


# Create your views here.
@login_required(login_url='/login')
def index(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        starred         = QuizFileSystem.objects.filter(starred=1, active=True, owner=request.user.id).count()
        sharred         = len(eval(request.user.shared_with_me))
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        recent          = QuizFileSystem.objects.filter(active=True, owner=request.user.id, file_type="Quiz").order_by('-last_opened')[:4]
        folders         = QuizFileSystem.objects.filter(active=True, owner=request.user.id, folder= 0, file_type="folder").order_by(fryp)
        all_files       = QuizFileSystem.objects.filter(active=True, owner=request.user.id, folder=0, file_type="Quiz",).order_by(fry)
        path            = "quiz/" + mode + "/Quiz.html"
        

        if len(all_files) > 4:
            files = []
            for a_file in all_files:
                if a_file in recent:
                    pass
                else:
                    files.append(a_file)
            all_files = files

        context = {
            'short_name': sname,
            'starred'   : starred,
            'sharred'   : sharred,
            'recent'    : recent,
            'folders'   : folders,
            'files'     : all_files,
            'state'     : state,
            "filt"      : filt,
            "folt"      : folt,
        }
    else:
        return redirect("/login")

    return render(request, path, context)


@login_required(login_url='/login')
def quiz_attempt(request, file_id):
    sname = None
    if (request.user.is_authenticated):
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        tid             = int(file_id)
        path            = "quiz/" + mode + "/quiz-attempt.html"
        qs              = FileSystem.objects.filter(pk=tid, active=True, owner=request.user).first()

        if qs is None:
            raise Http404("File does not exist")
        else:
            filename        = qs.name
            if qs.quized_saved:
                qz      = QuizFileSystem.objects.filter(note_from=qs, active=True, owner=request.user).first()
                output  = os.path.join(media_root, str(qz.location))
            else:
                output          = os.path.join(BASE_DIR+'/templates/', 'notes/Questions/' + filename + "-" + "evaluation_questions.json")
            with open(output, 'r+') as file:
                questions_answers_list = json.load(file)
            context = {
                'filename'      : filename,
                'file_id'       : tid,
                'questions'     : questions_answers_list,
                'saved'         : qs.quized_saved,
                'qf'            : qs
            }
        
    else:
        return redirect("/login")

    return render(request, path, context)


@login_required(login_url='/login')
def save_quiz(request):
    data = {}
    file_id     = int(request.GET.get('note_id'))
    file_name   = request.GET.get('note_name').strip()
    quiz_type   = request.GET.get('quiz_type')
    start_date  = request.GET.get('start_date')
    end_date    = request.GET.get('end_date')
    info        = request.GET.get('info')
    quiz_taken  = request.GET.get('taken')
    
    if (request.user.is_authenticated):
        quiz_model  = QuizFileSystem()
        output      = os.path.join(BASE_DIR+'/templates/', 'notes/Questions/' + file_name + "-" + "evaluation_questions.json")
        statinfo    = os.stat(output)
        fileSize    = statinfo.st_size
        note_from   = FileSystem.objects.get(pk=file_id)
        name, ext   = os.path.splitext(output)
        quiz_name   = file_name + " Quiz"
        qs          = QuizFileSystem.objects.filter(name=file_name, owner=request.user, active=True)
        user_state  = UserState.objects.get(user=request.user)
                
        if ext == ".json" and qs is None or qs.exists() == False:
            note_from.quized_saved = True
            note_from.quized       = True
            note_from.save()
            prev_size                   = user_state.total_storage
            user_state.total_storage    = prev_size + fileSize
            user_state.save()
            with open(output) as file:   
                quiz_model.location.save(output, File(file))
            quiz_model.name             = quiz_name.capitalize()
            quiz_model.file_type        = "quiz_file"
            quiz_model.quiz_info        = info.split(",")
            quiz_model.size             = fileSize
            quiz_model.owner            = request.user
            quiz_model.note_from        = note_from
            
            quiz_model.last_editted_by  = request.user

            if quiz_taken == "false":
                quiz_model.taken_quiz       = False
            else:
                quiz_model.taken_quiz       = True

            if quiz_type != "":
                quiz_model.quiz_type    = quiz_type

            if start_date != "":
                date_object             = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
                quiz_model.start_date   =  date_object

            if end_date != "":
                date_object             = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
                quiz_model.end_date     =  date_object
            quiz_model.save()

            if note_from.folder != 0:
                quiz_folder                  = QuizFileSystem()
                copy_folder                 = FileSystem.objects.get(pk=note_from.folder)
                quiz_folder.name             = copy_folder.name
                quiz_folder.file_type        = "quiz_folder"
                quiz_folder.size             = fileSize
                quiz_folder.owner            = request.user
                quiz_folder.note_from        = note_from
                quiz_folder.last_editted_by  = request.user
                quiz_folder.save()

                quiz_model.folder             = quiz_folder.id
                quiz_model.save()                
                
            os.remove(output)
            data["url"] =  "/Dashboard"
            data["msg"] = "Operation Successful, Quiz Saved"
            return JsonResponse(data)
        else:
            data["error"] = "Quiz File already exits in database"
            return JsonResponse(data)
        


    else:
        return redirect("/login")
        
    return JsonResponse(data)



