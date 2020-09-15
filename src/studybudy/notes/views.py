import json, os, re, pytz, random, pdfkit 
import time, mimetypes
from datetime import datetime
from django.utils import timezone
from .utils.converter import Converter
from .utils.determine_state import DetermineState
from .utils.remove_share import RemoveShare
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wsgiref.util import FileWrapper
from studybudy.settings import BASE_DIR
from .models import FileSystem
from users.models import UserState
from .app import Application


media_root = settings.MEDIA_ROOT
Users = get_user_model()

# Create your views here.
@login_required(login_url='/login')
def index(request):
    
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        starred         = FileSystem.objects.filter(starred=1, active=True, owner=request.user.id).count()
        sharred         = len(eval(request.user.shared_with_me))
        DS              = DetermineState(state)

        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        recent          = FileSystem.objects.filter(active=True, owner=request.user.id, file_type="file").order_by('-last_opened')[:4]
        folders         = FileSystem.objects.filter(active=True, owner=request.user.id, folder= 0, file_type="folder").order_by(fryp)
        all_files       = FileSystem.objects.filter(active=True, owner=request.user.id, folder=0, file_type="file",).order_by(fry)
        path            = "notes/" + mode + "/index.html"
        

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
@csrf_exempt
def upload_notes(request):
    data = {}
    if (request.user.is_authenticated):
        user_state  = UserState.objects.get(user=request.user)
        file_model  = FileSystem()
        _, file     = request.FILES.popitem()  # get first element of the uploaded files
        fold        = request.POST.get('fold')
        # print(fold)

           
        for f in file:
            file_name = f.name
            name, ext = os.path.splitext(file_name)
            qs        = FileSystem.objects.filter(name=name, owner=request.user, active=True)
            print(qs)
            
            
            if ext == ".pdf":
                if qs is None and  qs.exists() == False:
                    file_model.name             = name.capitalize()
                    file_model.location         = f
                    file_model.file_type        = "file"
                    file_model.owner            = request.user
                    file_model.last_editted_by  = request.user
                    file_model.size             = f.size
                    if fold and fold != "undefined":
                        file_model.folder   = int(fold)
                    file_model.save()
                    prev_size                   = user_state.total_storage
                    user_state.total_storage    = prev_size + f.size
                    user_state.save()
                else:
                    data["error"] = "File Input is invalid, File already exist in Database"
                    return JsonResponse(data)
            else:
                data["error"] = "File Input is invalid, Only PDF files Allowed"
                return JsonResponse(data)

        data['url'] = "/Dashboard"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url='/login')
def create_newFolder(request):
    folder_name = request.GET.get('filename')
    description = request.GET.get('description')
    ids         = request.GET.get('id')
    file_model = FileSystem()
    data = {}

    if (request.user.is_authenticated):
        qs = FileSystem.objects.filter(name=folder_name, owner=request.user, active= True)
        fd = FileSystem.objects.filter(active=True, owner=request.user, id=ids, file_type="folder").first()
        fdr = FileSystem.objects.filter(active=True, id=ids, file_type="folder").first()
        picolo = re.match("/^(?:[A-Za-z]+)(?:[A-Za-z0-9 _-]*)$/", str(folder_name))
        ricolo = re.match("/^[A-Za-z0-9.\s_-]*$/", str(description))

        if qs is not None and qs.exists() == True:
            data["error"] = "Folder Input name is invalid"
            return JsonResponse(data)
        elif picolo == False or ricolo == False:
            data["error"] = "Folder Input name  is invalid"
            return JsonResponse(data)
        if ids is not None:
            if fdr.shared_with is None or fdr.shared_with == "":
                fsw = []
            else:
                fsw = eval(fdr.shared_with)
            if fd is None and str(request.user.id) not in fsw:
                data["error"] = "You are not allowed to accees this folder"
                return JsonResponse(data)
            elif str(request.user.id) in fsw and fdr.public == False:
                data["error"] = "You are not allowed to accees this folder"
                return JsonResponse(data)
            elif str(request.user.id) in fsw and fdr.public == True:
                sw                      = []
                sw.append(str(fdr.owner.id))
                if ids is not None:
                    file_model.folder = int(ids)
                file_model.name         = str(folder_name)
                file_model.file_type    = "folder"
                file_model.owner        = request.user
                file_model.shared_with  = sw
                file_model.description  = description
                file_model.save()
            else: 
                file_model.folder = int(ids)
                file_model.name         = str(folder_name)
                file_model.file_type    = "folder"
                file_model.owner        = request.user
                file_model.description  = description
                file_model.save()
        else:
            file_model.name         = str(folder_name)
            file_model.file_type    = "folder"
            file_model.owner        = request.user
            file_model.description  = description
            file_model.save()


        data['url'] = "/Dashboard"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url='/login')
def create_newFile(request):

    file_name   = request.GET.get('fileName').capitalize()
    description = request.GET.get('description')
    fileType    = request.GET.get('fileType')
    fold        = request.GET.get('fold')
    file_model  = FileSystem()
    picolo = re.match("/^(?:[A-Za-z]+)(?:[A-Za-z0-9 _-]*)$/", str(file_name))
    ricolo = re.match("/^[A-Za-z0-9.\s_-]*$/", str(description))
    
    data = {}

    if (request.user.is_authenticated):
        qs = FileSystem.objects.filter(name=file_name, owner=request.user, active=True)

        if qs is not None and qs.exists() == True:
            data["error"] = "File Input name is invalid, already exist"
            return JsonResponse(data)
        elif picolo == False or ricolo == False:
            data["error"] = "File Input name  is invalid"
            return JsonResponse(data)
        else:
            file_model.name         = str(file_name)
            file_model.file_type    = fileType
            file_model.owner        = request.user
            file_model.description  = description
            if fold:
                file_model.folder   = int(fold)
            file_model.save()

            data['msg'] = fileType.capitalize() + " created successfully"
        

        data['url'] = "/Dashboard"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
def rename_File(request):
    file_name   = request.GET.get('fileName').capitalize()
    description = request.GET.get('description')
    fileType    = request.GET.get('fileType')
    ID          = request.GET.get('ID')
    picolo = re.match("/^(?:[A-Za-z]+)(?:[A-Za-z0-9 _-]*)$/", str(file_name))
    ricolo = re.match("/^[A-Za-z0-9.\s_-]*$/", str(description))
    
    data = {}

    if (request.user.is_authenticated):
        file_model  = FileSystem.objects.get(pk=int(ID))
        qs = FileSystem.objects.filter(name=file_name, owner=request.user, active=True)

        if file_model is None:
            data["error"] = "Something went wrong, please try again"
            return JsonResponse(data)
        elif picolo == False or ricolo == False:
            data["error"] = "File Input name  is invalid"
            return JsonResponse(data)
        else:
            file_model.name         = str(file_name)
            file_model.file_type    = fileType
            file_model.owner        = request.user
            file_model.description  = description
            file_model.save()
            data['msg'] = fileType.capitalize() + " Renamed successfully"
        

        data['url'] = "/Dashboard"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
def get_details(request):
    pk = request.GET.get('ID')
    data = {}

    if (request.user.is_authenticated):
        qs      = FileSystem.objects.get(pk=int(pk))
        fl      = FileSystem.objects.filter(active=True, owner=request.user, id=int(pk)).first()
        
        if qs is None:
            data["error"] = "Something Went Wrong, Please Try Again"
            return JsonResponse(data)
        # elif fl is None:
        #     data["error"] = "You are not allowed to access this file"
        #     return JsonResponse(data)
        else:
            data['id']          = str(pk)
            data['file_name']   = str(qs.name)
            data['size']        = str(qs.size)
            data['location']    = str(qs.location)
            data['created']     = qs.date_created.strftime("%H:%M:%S - %b %d %Y")
            if qs.description == None:
                data['description'] = ""
            else:
                data['description'] = str(qs.description)
            if qs.file_type == "file":
                data['file_type']   = "PDF file"
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


@login_required(login_url="/login")
def change_description(request):
    data = {}
    active_id = int(request.GET.get('ID'))
    desc = request.GET.get('desc')

    if (request.user.is_authenticated):
        active_file = FileSystem.objects.get(pk=active_id)
        fl      = FileSystem.objects.filter(active=True, owner=request.user, id=active_id).first()

        if active_file is None:
            data['error'] = "Sorry something went wrong description not added Successfully"
            return JsonResponse(data)
        elif fl is None:
            data["error"] = "You are not allowed to access this file"
            return JsonResponse(data)
        else:
            active_file.description = desc
            active_file.save()
            data['msg'] = "Description Editted Successfully"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
def make_public(request):
    data = {}
    active_id = int(request.GET.get('ID'))
    active_status = request.GET.get('status')
    
    if active_status == "True":
        active_status = True
    else:
        active_status = False

    if (request.user.is_authenticated):
        active_file = FileSystem.objects.get(pk=active_id)
        fl      = FileSystem.objects.filter(active=True, owner=request.user, id=active_id).first()

        if active_file is None:
            data['msg'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        elif fl is None:
            data['msg'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        else:
            active_file.public = active_status
            active_file.save()
            typ = active_file.file_type.capitalize()
        
            if active_file.public == False:
                data['msg'] = typ + " made Private"
            else:
                data['msg'] = typ + " made Public"
    else:
        return redirect("/login")
            
    return JsonResponse(data)


@login_required(login_url="/login")
def star_file(request):
    data = {}
    active_id = int(request.GET.get('ID'))
    active_status = request.GET.get('status')

    if active_status == "True":
        active_status = True
    else:
        active_status = False

    if (request.user.is_authenticated):
        active_file = FileSystem.objects.get(pk=active_id)
        fl          = FileSystem.objects.filter(active=True, owner=request.user, id=active_id).first()


        if active_file is None:
            data['msg'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        elif fl is None:
            data['msg'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        else:
            active_file.starred = active_status
            active_file.save()

            if active_file.starred:
                data['msg'] = active_file.file_type.capitalize() + " has been starred"
            else:
                data['msg'] = active_file.file_type.capitalize() + " has been un-starred"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
@csrf_exempt
def share_file(request):
    data = {}
    emailArray      = request.POST.get('emails')
    message         = request.POST.get('note')
    file_id         = int(request.POST.get('ID'))
    failed          = []
    emailArray      = emailArray.split(",")

    if (request.user.is_authenticated):
        fl          = FileSystem.objects.filter(active=True, owner=request.user, id=file_id).first()
        if fl is None:
            data["error"] = "Not Allowed to share File"
            return JsonResponse(data)
        elif len(emailArray) > 0 and file_id != "" and fl is not None:
            for person in emailArray:
                if person != "":
                    person_inst = Users.objects.filter(Q(email = person.strip()) | Q(username = person.strip()))
                    file_shared = FileSystem.objects.filter(pk=int(file_id)).first()

                    if person_inst.exists() and person_inst.first() != request.user:
                        find_id = person_inst.values_list('id', flat=True)
                        psn     = Users.objects.get(pk=int(find_id[0]))

                        if psn.shared_with_me == None:
                            file_list = []
                            file_list.append(file_id)
                            psn.shared_with_me = file_list
                            psn.save()
                        else:
                            already_list = eval(psn.shared_with_me)
                            if str(file_id) not in already_list:
                                already_list.append(str(file_id))
                            else:
                                pass
                            psn.shared_with_me = already_list
                            psn.save()

                        if file_shared.shared_with == None:
                            id_list = []
                            id_list.append(str(find_id[0]))
                            # print(id_list)
                            file_shared.sharable    = True
                            file_shared.shared_with = id_list
                            file_shared.save()
                        else:
                            former = eval(file_shared.shared_with)
                            if str(find_id[0]) not in former:
                                former.append(str(find_id[0]))
                            else:
                                pass
                            file_shared.sharable    = True
                            file_shared.shared_with = former
                            file_shared.save()

                        if file_shared.file_type == "folder":
                            contents = FileSystem.objects.filter(active=True, owner=request.user, folder=int(file_shared.id))
                            for content in contents:
                                    if content.shared_with == None:
                                        id_list = []
                                        id_list.append(str(find_id[0]))
                                        # print(id_list)
                                        content.sharable    = True
                                        content.shared_with = id_list
                                        content.save()
                                    else:
                                        former = eval(content.shared_with)
                                        if str(find_id[0]) not in former:
                                            former.append(str(find_id[0]))
                                        else:
                                            pass
                                        content.sharable    = True
                                        content.shared_with = former
                                        content.save()
                        else:
                            pass
                    else:
                        failed.append(person)
                
            if (len(failed) == 0):
                data['url'] = "/Dashboard"
            else:
                listj  = ",".join(failed)
                data["error"] = "The following recipient addreess or username is invalid " + listj
        else:
            data["error"] = "No recipient recieved"
    else:
        return redirect("/login")
        

    return JsonResponse(data)


@login_required(login_url="/login")
def open_file(request):
    data            = {}
    response        = {}
    cv              = Converter()
    file_id         = request.GET.get('ID')

    if (request.user.is_authenticated):
        qs = FileSystem.objects.filter(pk=int(file_id), active=True, owner=request.user, file_type="file").first()
        fl = FileSystem.objects.filter(pk=int(file_id), active=True, file_type="file").first()

        if fl.shared_with is None or fl.shared_with == "":
            fsw = []
        else:
            fsw = eval(fl.shared_with)

        if qs is None and str(request.user.id) not in fsw:
            data["error"] = "You are not allowed to accees this file"
            return JsonResponse(data)

        if str(request.user.id) in fsw or qs is not None:
            if qs is not None:
                fs = qs
            if qs is None and fl is not None and str(request.user.id) in fsw:
                fs = fl

    
            fp = str(fs.location)
            if fp != "":
                url = os.path.join(media_root, fp)
            else:
                now = timezone.now()
                fs.last_opened = now
                fs.save()
                data['new_file'] = "empty file"
                return JsonResponse(data)

            if os.path.exists(url):
                now = timezone.now()
                fs.last_opened = now
                fs.save()
                feey = os.path.join(media_root, "Notes\output_2.html")
                html = cv.pdf_to_html(url, feey)
                Html_file = open(html,"r")
                forbidin = [4, 5]
                line_no = 1
                rery = []
                for line in Html_file.read().splitlines():
                    if line_no not in forbidin:
                        rery.append(line)
                    line_no += 1
                text = ''.join(rery[:-2])
                text += '<br></span></div></body></html>'
                # print(text)
                response  = HttpResponse(text, content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(url)
                Html_file.close()
                os.remove(html)
                return response
            else:
                data['error'] = "Cannot find file"
        else:
            data['error'] = "You are not allowed to view this file"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
def open_File(request, file_id):
    data            = {}
    response        = {}
    cv              = Converter()
    file_id         = file_id
    sname           = request.user.get_short_name()
    state           = UserState.objects.filter(user=request.user).first()
    DS              = DetermineState(state)
    mode            = DS.determine_mode()
    path            = "notes/" + mode + "/previewNote.html"

    if (request.user.is_authenticated):
        qs = FileSystem.objects.filter(pk=int(file_id), active=True, owner=request.user, file_type="file").first()
        fl = FileSystem.objects.filter(pk=int(file_id), active=True, file_type="file").first()

        if fl.shared_with is None or fl.shared_with == "":
            fsw = []
        else:
            fsw = eval(fl.shared_with)

        if qs is None and str(request.user.id) not in fsw:
            data["error"] = "You are not allowed to accees this file"
            return JsonResponse(data)

        if str(request.user.id) in fsw or qs is not None:
            if qs is not None:
                fs = qs
            if qs is None and fl is not None and str(request.user.id) in fsw:
                fs = fl

    
            fp = str(fs.location)
            if fp != "":
                url = os.path.join(media_root, fp)
            else:
                now = timezone.now()
                fs.last_opened = now
                fs.save()
                data['new_file'] = "empty file"
                return JsonResponse(data)

            if os.path.exists(url):
                now = timezone.now()
                fs.last_opened = now
                fs.save()
                feey = os.path.join(media_root, "Notes\output_2.html")
                html = cv.pdf_to_html(url, feey)
                Html_file = open(html,"r")
                forbidin = [4, 5]
                line_no = 1
                rery = []
                for line in Html_file.read().splitlines():
                    if line_no not in forbidin:
                        rery.append(line)
                    line_no += 1
                text = ''.join(rery[:-2])
                text += '<br></span></div></body></html>'
                # print(text)
                response  = HttpResponse(text, content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(url)
                Html_file.close()
                os.remove(html)
                fext    = []
                fext.append(text)
                fext.append(fs.id)
                context = {
                    'short_name': sname,
                    'fileName'  : fs.name,
                    'data'      : fext
                }
            else:
                context = {
                    'short_name': sname,
                    'fileName'  : fs.name,
                    'error'      : "Cannot find file",
                }
 
        else:
            context = {
                    'short_name': sname,
                    'fileName'  : fs.name,
                    'error'     : "You are not allowed to view this file",
                }
    else:
        return redirect("/login")
        
    
    return render(request, path, context)


@login_required(login_url="/login")
@csrf_exempt
def save_file(request):
    data                = {}
    file_id             = request.POST.get('file_id')
    file_data           = request.POST.get('file_data')
    options             = {
                            'page-size': 'A4',
                            'margin-top': '0.75in',
                            'margin-right': '0.75in',
                            'margin-bottom': '0.75in',
                            'margin-left': '0.75in',
                        }
    # print(file_data)
    if (request.user.is_authenticated):
        qs = FileSystem.objects.filter(pk=int(file_id), active=True, owner=request.user, file_type="file").first()
        fl = FileSystem.objects.filter(pk=int(file_id), active=True, file_type="file").first()
        user_state  = UserState.objects.get(user=request.user)
        
        if fl.shared_with is None or fl.shared_with == "":
            fsw = []
        else:
            fsw = eval(fl.shared_with)

        if qs is None and str(request.user.id) not in fsw:
            data["error"] = "You are not allowed to Edit this file"
            return JsonResponse(data)
        elif str(request.user.id) in fsw and fl.public == False:
            data["error"] = "You are not allowed to Edit this file"
            return JsonResponse(data)
        elif str(request.user.id) in fsw and fl.public == True:
            
            if qs is not None:
                fs = qs
            if qs is None and fl is not None and str(request.user.id) in fsw:
                fs = fl
            
            fp              = str(fs.location)
            new_filename    = random.randint(1,3910209312)
            final_filename  = '{new_filename}{ext}'.format(new_filename=new_filename, ext=".pdf")
            pathy           = os.path.join(BASE_DIR+'/templates/', 'notes/PDF/output_pdf.html')

            if fp != "":        
                path            = fp
                pathr           = os.path.join(media_root, fp)
                directory       = os.path.dirname(pathr) 
                file_created    = os.path.join(directory, final_filename)
                os.remove(pathr)

                try:
                    Html_file           = open(pathy,"w")
                    Html_file.write(str(file_data).encode('cp850','replace').decode('cp850'))
                    Html_file.close()
                    pdfkit.from_file(pathy, file_created, options=options)
                    statinfo            = os.stat(file_created)
                    fileSize            = statinfo.st_size
                    now                 = timezone.now()
                    fs.location         = file_created
                    fs.last_editted     = now
                    fs.last_editted_by  = request.user
                    fs.size             = fileSize
                    fs.save()
                    prev_size                   = user_state.total_storage
                    user_state.total_storage    = prev_size + fileSize
                    user_state.save()
                except e as error:
                    data["error"] = "File save was not successful"
                    return JsonResponse(data)
                
                fold                    = fs.folder
                while fold != 0:
                    now                 = timezone.now()
                    fl                  = FileSystem.objects.get(pk=fold)
                    SZ                  = fl.size
                    fl.size             = SZ + fileSize
                    fl.last_editted     = now
                    fl.last_editted_by  = request.user
                    fold                = fl.folder
                    fl.save()
                data["success"] = "File has been saved successfully"
                return JsonResponse(data)

            else:
                directory           = "Notes\{new_filename}".format(new_filename=new_filename)
                path                = os.path.join(media_root, directory) 
                file_created        = os.path.join(path, final_filename)
                Html_file           = open(pathy,"w")
                os.mkdir(path)

                try:
                    Html_file.write(str(file_data).encode('cp850','replace').decode('cp850'))
                    Html_file.close()
                    pdfkit.from_file(pathy, file_created, options=options)
                    statinfo            = os.stat(file_created)
                    fileSize            = statinfo.st_size
                    now                 = timezone.now()
                    fs.location         = file_created
                    fs.last_editted     = now
                    fs.last_editted_by  = request.user
                    fs.size             = fileSize
                    fs.save()
                    prev_size                   = user_state.total_storage
                    user_state.total_storage    = prev_size + fileSize
                    user_state.save()
                except e as error:
                    data["error"] = "File save was not successful"
                    return JsonResponse(data)

                fold                    = fs.folder
                while fold != 0:
                    now                 = timezone.now()
                    fl                  = FileSystem.objects.get(pk=fold)
                    SZ                  = fl.size
                    fl.size             = SZ + fileSize
                    fl.last_editted     = now
                    fl.last_editted_by  = request.user
                    fold                = fl.folder
                    fl.save()
                data["success"] = "File has been saved successfully"
                return JsonResponse(data)
                
        else:
            fs              = qs
            fp              = str(fs.location)
            new_filename    = random.randint(1,3910209312)
            final_filename  = '{new_filename}{ext}'.format(new_filename=new_filename, ext=".pdf")
            pathy           = os.path.join(BASE_DIR+'/templates/', 'notes/PDF/output_pdf.html')

            if fp != "":
                path            = fp
                pathr           = os.path.join(media_root, fp)
                directory       = os.path.dirname(pathr) 
                file_created    = os.path.join(directory, final_filename)
                os.remove(pathr)

                
                Html_file           = open(pathy,"w")
                Html_file.write(str(file_data).encode('cp850','replace').decode('cp850'))
                Html_file.close()
                pdfkit.from_file(pathy, file_created, options=options)
                statinfo                = os.stat(file_created)
                fileSize                = statinfo.st_size
                now                     = timezone.now()
                fs.location             = file_created
                fs.last_editted         = now
                fs.last_editted_by      = request.user
                fs.size                 = fileSize
                fs.save()
                prev_size                   = user_state.total_storage
                user_state.total_storage    = prev_size + fileSize
                user_state.save()
                # except:
                #     data["error"] = "File save was not successful"
                #     return JsonResponse(data)
                
                fold                        = fs.folder
                while fold != 0:
                    now                     = timezone.now()
                    fl                      = FileSystem.objects.get(pk=fold)
                    SZ                      = fl.size
                    fl.size                 = SZ + fileSize
                    fl.last_editted         = now
                    fl.last_editted_by      = request.user
                    fold                        = fl.folder
                    fl.save()
                    
                data["success"] = "File has been saved successfully"
                return JsonResponse(data)
    
            else:
                directory           = "Notes\{new_filename}".format(new_filename=new_filename)
                path                = os.path.join(media_root, directory) 
                file_created        = os.path.join(path, final_filename)
                Html_file           = open(pathy,"w")
                os.mkdir(path)

                # try:
                Html_file.write(str(file_data).encode('cp850','replace').decode('cp850'))
                Html_file.close()
                pdfkit.from_file(pathy, file_created, options=options)
                statinfo            = os.stat(file_created)
                fileSize            = statinfo.st_size
                now                 = timezone.now()
                fs.location         = file_created
                fs.last_editted     = now
                fs.last_editted_by  = request.user
                fs.size             = fileSize
                fs.save()
                prev_size                   = user_state.total_storage
                user_state.total_storage    = prev_size + fileSize
                user_state.save()
                # except e as error:
                #     data["error"] = "File save was not successful"
                #     return JsonResponse(data)

                fold                    = fs.folder
                while fold != 0:
                    now                 = timezone.now()
                    fl                  = FileSystem.objects.get(pk=fold)
                    SZ                  = fl.size
                    fl.size             = SZ + fileSize
                    fl.last_editted     = now
                    fl.last_editted_by  = request.user
                    fold                = fl.folder
                    fl.save()
                    
                data["success"] = "File has been saved successfully"
                return JsonResponse(data)
    else:
        return redirect("/login")
        

    return JsonResponse(data)


@login_required(login_url="/login")
def delete_file(request):
    data = {}
    active_id   = request.GET.get('file_id')
    # print(active_id)
    if (request.user.is_authenticated):
        active_file = FileSystem.objects.get(pk=int(active_id))
        rs          = RemoveShare()
        loop_list   = []
        fl          = FileSystem.objects.filter(active=True, owner=request.user, id=int(active_id)).first()


        if active_file is None:
            data['error'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        elif fl is None:
            data['error'] = "Sorry something went wrong during handlling of operation"
            return JsonResponse(data)
        else:
            active_type = active_file.file_type
            if active_type == "file":
                active_file.active = False
                active_file.sharable = False
                if active_file.shared_with is not None and active_file.shared_with != "":
                    sw = eval(active_file.shared_with)
                    tk = rs.remove_shared_rigth(sw, active_file.id)
                    if tk :
                        active_file.shared_with = ""

                active_file.save()
                tik = active_file.folder
                if tik != 0:
                    sz          = active_file.size
                    fdr         = FileSystem.objects.get(pk=int(tik))
                    fdr_Sz      = fdr.size
                    fold        = fdr.folder
                    fdr.size    = fdr_Sz - sz
                    fdr.save()
                    while fold != 0:
                        fl          = FileSystem.objects.get(pk=fold)
                        trn         = fl.size
                        fl.size     = trn - sz
                        fold        = fl.folder 
                        fl.save() 
                data["success"] = "File successfully deleted"
            if active_type == "folder":
                active_file.active = False
                active_file.sharable = False
                if active_file.shared_with is not None and active_file.shared_with != "":
                    print(active_file.shared_with)
                    sw = eval(active_file.shared_with)
                    tk = rs.remove_shared_rigth(sw, active_file.id)
                    if tk :
                        active_file.shared_with = ""
                active_file.save()
                active_sub_file = FileSystem.objects.filter(folder=active_id)
                loop_list.append(active_sub_file)
                while len(loop_list) != 0:

                    for sub in loop_list[0]:
                        sub.active = False
                        sub.sharable = False
                        if sub.shared_with is not None and sub.shared_with != "":
                            sw = eval(sub.shared_with)
                            print(sub.id)
                            tk = rs.remove_shared_rigth(sw, sub.id)
                            if tk :
                                sub.shared_with = ""
                        sub.save()
                        if sub.file_type == "folder":
                            sub_sub_file = FileSystem.objects.filter(folder=int(sub.id))
                            loop_list.append(sub_sub_file)
                    loop_list.pop(0)
                tik = active_file.folder
                if tik != 0:
                    sz          = active_file.size
                    fdr         = FileSystem.objects.get(pk=int(tik))
                    fdr_Sz      = fdr.size
                    fold        = fdr.folder
                    fdr.size    = fdr_Sz - sz
                    fdr.save()
                    while fold != 0:
                        fl          = FileSystem.objects.get(pk=fold)
                        trn         = fl.size
                        fl.size     = trn - sz
                        fold        = fl.folder 
                        fl.save()
                data["success"] = "Folder successfully deleted"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url="/login")
def quiz_note(request):
    data = {}
    file_id = int(request.GET.get('ID'))
    if (request.user.is_authenticated):
        fl = FileSystem.objects.get(pk=file_id)
        if fl is not None:
            fs = str(fl.location)
            filename = fl.name
            fp = os.path.join(media_root, fs)
            start_time = time.time()
            cv = Converter()
            okay, words, text = cv.get_pdf_text(fp)
            if okay:
                apps = Application()
                question_ans, info, total = apps.ques_application(text, filename)
                end_time = time.time()
                print("Running Time: ", end_time-start_time)
                data["OK"]      = "Operation Successful, quiz generated"
                data['words']   = words
                data['total']   = total
                data['result']  = info
                data["time"]    = end_time-start_time
                data["file_id"] = file_id
                data["saved"]   = fl.quized_saved
                fl.words        = words
                fl.time_taken   = int(end_time-start_time)
                # fl.quized       = True
                fl.save()
            else:
                data['error'] = text

        else:
            data['error'] = "Somethinf Went wrong, please try again"
    else:
        return redirect("/login")
        

    return JsonResponse(data)


@login_required(login_url="/login")
def summarize(request):
    data = {}
    file_id = int(request.GET.get('ID'))
    number  = int(request.GET.get('number'))

    if (request.user.is_authenticated):
        fl = FileSystem.objects.get(pk=file_id)
        if fl is not None:
            fs = str(fl.location)
            filename = fl.name
            fp = os.path.join(media_root, fs)
            cv = Converter()
            okay, words, text = cv.get_pdf_text(fp)
            if okay:
                apps = Application()
                summary = apps.summary_application(text[0], number)
                data["fileName"] = filename
                data["summary"]  = summary
            else:
                data['error'] = text
        else:
            data['error'] = "Somethinf Went wrong, please try again"
    else:
        return redirect("/login")

    return JsonResponse(data)


@login_required(login_url="/login")
def quiz_result(request):
    data = {}
    file_id = int(request.GET.get('file_id'))
    if (request.user.is_authenticated):
        fl = FileSystem.objects.get(pk=file_id)
        if fl is not None:
            cv              = Converter()
            filename        = fl.name
            if fl.quized_saved:
                print(fl.name)
                qzy  = QuizFileSystem.objects.filter(note_from=fl, active=True, owner=request.user).first()
                output  = os.path.join(media_root, str(qzy.location))
            else:
                output          = os.path.join(BASE_DIR+'/templates/', 'notes/Questions/' + filename + "-" + "evaluation_questions.json")

            with open(output, 'r+') as file:
                questions_answers_list = json.load(file)
            total, result = cv.count_questions(questions_answers_list)
            data["OK"]      = "Operation Successful, quiz generated"
            data['words']   = fl.words
            data['total']   = total
            data['result']  = result
            data["time"]    = fl.time_taken
            data["file_id"] = file_id
            data["saved"]   = fl.quized_saved

        else:
            data['error'] = "Somethinf Went wrong, please try again"
    else:
        return redirect("/login")
        

    return JsonResponse(data)


@login_required(login_url='/login')
def filter_note(request):
    data = {}
    active_id = request.user
    active_type = request.GET.get('type')
    active_status = request.GET.get('filter')

    if (request.user.is_authenticated):
        active_user = UserState.objects.get(user=active_id)
        active_use = Users.objects.get(email=active_id)
        if active_user is not None:
            if active_use.active :
                if active_type == "file":
                    active_user.file_filters = active_status
                    active_user.save()
                elif active_type == "tab":
                    active_user.file_filters = active_status
                    active_user.folder_filters = active_status
                    active_user.save()
                else:
                    active_user.folder_filters = active_status
                    active_user.save()
            else:
                data['msg'] = "Sorry something went wrong during handlling of operation"
        else:
            data['msg'] = "Sorry something went wrong during handlling of operation"
    else:
        return redirect("/login")
        
    return JsonResponse(data)


@login_required(login_url='/login')
def order_note(request, order_id):
    data = {}
    active_id = request.user
    active_type = order_id


    if (request.user.is_authenticated):
        active_user = UserState.objects.get(user=active_id)
        active_use = Users.objects.get(email=active_id)

        if active_user is not None:
            if active_use.active :
                if active_type == "file":
                    status      = active_user.file_order
                    if status == "ASC":
                        active_status = "DESC"
                    else:
                        active_status = "ASC"
                    active_user.file_order = active_status
                    active_user.save()
                else:
                    status      = active_user.folder_order
                    if status == "ASC":
                        active_status = "DESC"
                    else:
                        active_status = "ASC"
                    active_user.folder_order = active_status
                    active_user.save()

            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("/login")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def change_view(request, view_id):
    data = {}
    active_id = request.user
    active_status = str(view_id)

    if (request.user.is_authenticated):
        active_user = UserState.objects.get(user=active_id)
        active_use = Users.objects.get(email=active_id)
        
        if active_user is not None:
            if active_use.active :
                active_user.view = active_status
                active_user.save()
                if active_status == "tabular" and active_user.file_filters == "Name" or active_user.folder_filters == "Name":
                    active_user.file_filters = "Last Modified"
                    active_user.folder_filters = "Last Modified"
                    active_user.save()
                    
            else:
                data['msg'] = "Sorry something went wrong during handlling of operation"
        else:
            data['msg'] = "Sorry something went wrong during handlling of operation"
    else:
        return redirect("/login")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/login")
def stared(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        folders         = FileSystem.objects.filter(active=True, starred=True, owner=request.user.id, folder= 0, file_type="folder").order_by(fryp)
        all_files       = FileSystem.objects.filter(active=True, starred=True, owner=request.user.id, file_type="file",).order_by(fry)
        path            = "notes/" + mode + "/stared.html"

        context = {
            'short_name': sname,
            'folders'   : folders,
            'files'     : all_files,
            'state'     : state,
            'filt'      : filt,
            'folt'      : folt,
        }
    else:
        return redirect("/login")
        
    return render(request, path, context)


@login_required(login_url="/login")
def shared(request):
    sname = None
    if (request.user.is_authenticated):
        sname           = request.user.get_short_name()
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        items           = eval(request.user.shared_with_me)
        pid             = request.user.id
        folders         = []
        files           = []

        if len(items) > 0:
            for it in items:
                f = FileSystem.objects.get(pk=int(it))
                sw = eval(f.shared_with)
                if str(pid) in sw:
                    if f.file_type == "folder" and f.active==True:
                        folders.append(f)
                    elif f.file_type == "file" and f.active == True:
                        files.append(f)
                    else:
                        pass
                else:
                    pass
        path            = "notes/" + mode + "/shared.html"
        # if state.file_filters == "ASC" or state.folder_filters == "ASC":
        #     files.sort()
        #     folders.sort()
        # else:
        #     pass
            # files.sort(reverse=True)
            # folders.sort(reverse=True)



        context = {
            'short_name': sname,
            'folders'   : folders,
            'files'     : files,
            'state'     : state,
            'filt'      : filt,
            'folt'      : folt,
        }
    else:
        return redirect("/login")
        
    return render(request, path, context)


@login_required(login_url='/login')
def move_list(request):
    data            = {}
    x               = []
    pk              = request.GET.get('ID')

    if (request.user.is_authenticated):
        qs      = FileSystem.objects.filter(active=True, owner=request.user, file_type="folder")
        qs2     = FileSystem.objects.get(pk=pk)

        if qs is None:
            data["error"] = "Something Went Wrong, Folders to move to do not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        else:
            for b in qs:
                if b.id != int(pk) and b.id != qs2.folder:
                    y = {}
                    y["id"]   = b.id
                    y["name"] = b.name
                    y["type"] = b.file_type
                    x.append(y) 
            
            data["src"] = x
            return JsonResponse(data)
        
    else:
        return redirect("/login")


@login_required(login_url='/login')
def move(request):
    pk_to             = request.GET.get('move_to')
    pk_moving             = request.GET.get('moving')
    data            = {}

    if (request.user.is_authenticated):
        q1      = FileSystem.objects.get(pk=int(pk_to))
        q2      = FileSystem.objects.get(pk=int(pk_moving))

        if q1 is None and q2 is None:
            data["error"] = "Something Went Wrong, Folder does not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        elif pk_to == pk_moving:
            data["error"] = "Something Went Wrong, Folder does not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        else:
            fld         = q1.folder
            fld_2       = q2.folder
            szl         = q2.size
            q2.folder   = q1.id 
            q2.save()
            q1.size     = int(q1.size) + szl
            q1.save()

            while fld != 0:
                new_q   = FileSystem.objects.get(pk=int(fld))

                if new_q is None :
                    data["error"] = "Something Went Wrong, Folder does not exist or you have no access to it Please Try Again"
                    return JsonResponse(data)
                else:
                    fld         = new_q.folder
                    new_q.size  = int(new_q.size) + szl
                    new_q.save()

            while fld_2 != 0:
                new_q   = FileSystem.objects.get(pk=int(fld_2))

                if new_q is None :
                    data["error"] = "Something Went Wrong, Folder does not exist or you have no access to it Please Try Again"
                    return JsonResponse(data)
                else:
                    fld_2         = new_q.folder
                    new_q.size  = int(new_q.size) - szl
                    new_q.save()



            data["success"] = "Operation Successful, " + q2.file_type + " have been moved"
            return JsonResponse(data)

    else:
        return redirect("/login")
    return JsonResponse(data)


@login_required(login_url='/login')
def download_file(request, file_id):
    pk              = int(file_id)
    data            = {}

    if (request.user.is_authenticated):
        q1      = FileSystem.objects.get(pk=pk)

        if q1 is None:
            data["error"] = "Something Went Wrong, Folder does not exist or you have no access to it Please Try Again"
            return JsonResponse(data)
        else:
            fp          = q1.location
            name_ext    = q1.name + ".pdf"
            fl_path = url = os.path.join(media_root, str(fp))
            print(fl_path)
            filename = name_ext

            # fl = open(fl_path, 'r', encoding="utf8", errors='ignore')
            fl = FileWrapper(open(fl_path,'rb'))
            # print(fl_path)
            mime_type, _ = mimetypes.guess_type(fl_path[0])
            print(mime_type)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response

    else:
        return redirect("/login")

    return JsonResponse(data)


@login_required(login_url="/login")
def folder_content(request, folder_id):
    context = {}
    sname = None
    press = None
    end   = "/folder_content.html"
    if (request.user.is_authenticated):
        fold_inst       = FileSystem.objects.filter(active=True, owner=request.user.id, id=folder_id, file_type="folder").first()
        fold_tint       = FileSystem.objects.filter(active=True, id=folder_id, file_type="folder").first()

        if fold_inst is None and fold_tint is None:
            raise Http404("Folder does not exist")
        elif fold_inst is None and fold_tint is not None:
            if fold_tint.shared_with != "" and fold_tint.shared_with is not None:
                sw  = eval(fold_tint.shared_with)
            else:
                sw = []
            if str(request.user.id) in sw:
                press = "Shared"
                # end   = "/shared.html"
                fold_inst = fold_tint
            else:
                raise Http404("Folder does not exist")
        else:
            if fold_inst is not None and fold_inst.starred:
                press = "Starred"
            else:
                press = None

        now = timezone.now()
        fold_inst.last_opened = now
        fold_inst.save()
        sname           = request.user.get_short_name()
        state           = UserState.objects.filter(user=request.user).first()
        DS              = DetermineState(state)
        fryp, fry       = DS.determine_order()
        filt, folt      = DS.determine_tab_filter()
        mode            = DS.determine_mode()
        starred         = FileSystem.objects.filter(starred=True, active=True, owner=request.user.id).count()
        sharred         = len(eval(request.user.shared_with_me))
        folders         = FileSystem.objects.filter(active=True, folder=folder_id, file_type="folder").order_by(fryp)
        all_files       = FileSystem.objects.filter(active=True,  folder=folder_id, file_type="file").order_by(fry)
        tree            = []
        fold            = fold_inst.folder
        path            = "notes/" + mode + end

        while fold != 0:
            dream = {}
            fl = FileSystem.objects.get(pk=fold)            
            dream["url"] = fl.id
            dream["data"] = fl.name
            tree.append(dream)
            fold = fl.folder
        tree.reverse()

        context = {
                'folder'    : fold_inst,
                'folder_id' : folder_id,
                'tree'      : tree,
                'short_name': sname,
                'starred'   : starred,
                'sharred'   : sharred,
                'folders'   : folders,
                'files'     : all_files,
                'state'     : state,
                'level'     : press,
                'filt'      : filt,
                'folt'      : folt,
                'press'     : press
        }
    else:
        return redirect("/login")
        
    return render(request, path, context)



