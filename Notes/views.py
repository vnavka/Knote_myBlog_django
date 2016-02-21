from django.shortcuts import render, render_to_response,redirect
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context ,RequestContext

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from Notes.models import KNote , Comments, UserImage
from django.db.models import Q

from django.conf import settings
from django.core.management import call_command

from datetime import datetime
from random import randint



# Create your views here.

def landing_page(request):
    args = {}
    args['user_name'] = auth.get_user(request).username
    return render_to_response('main_win.html',args,context_instance=RequestContext(request))

def statistic_page(request):
    args = {}
    args["is_adin"] = auth.get_user(request).is_superuser
    args["Users_reg"] = list(User.objects.filter()).__len__()
    args['user_name'] = auth.get_user(request).username
    args["top_note"] = KNote.objects.all().order_by('-knote_views')[0]
    args["top_user"] = User.objects.filter(username = str(args["top_note"].knote_host))[0]
    args["userimage"] = UserImage.objects.filter(user_image_host = args["top_user"] )[0]
    args["notes_base"] = list(KNote.objects.all()).__len__()
    args["comments_base"] = list(Comments.objects.all()).__len__()
    data = []
    users = User.objects.all()
    counter = 0
    for user in users:
        num_art = int(list(KNote.objects.filter(knote_host = user)).__len__())
        data.append([user,num_art,counter])
        counter+=1
    args["data"] = data
    return render_to_response('main_statistic.html',args)

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate( username = newuser_form.cleaned_data['username'],
                                         password = newuser_form.cleaned_data['password2'])
            auth.login(request,newuser)
            return redirect("/")
        else:
            args['form'] = newuser_form
    return render_to_response("register.html",args)

def test_registr(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.last_name = 'Lennon'
    user.save()
    return render_to_response("main_win.html")

def register_user_post(request):
    args = {}
    args = request.POST
    user = User.objects.create_user(args['login'],
                                    args['email'],
                                    args['pass'])
    #print args['login']
    user.last_name = args['name']
    user.save()
    # created_user = User.objects.filter(username = args['login'])[:1]
    image = UserImage(user_image_host = User.objects.get_by_natural_key(args['login']) )
    image.save()
    return redirect("/")

def login_user(request):
    args = {}
    args = request.POST
    if request.POST:

        user = auth.authenticate(username=args['login'], password=args['password'] )


        if user is not None:
            auth.login(request,user)
            # args['user_name_text'] = auth.get_user(request).username
            return redirect('/')
        else:
            args['login_error'] = "Couldn't find user"
            return render_to_response("main_win.html",args,context_instance=RequestContext(request))

    else:
        return render_to_response("main_win.html",args)

def logout_user(request):
    auth.logout(request)
    return redirect("/")

def show_user(request):
    args ={}
    args['user_name'] = auth.get_user(request).username
    args['username'] = auth.get_user(request).username
    args['userimage'] = UserImage.objects.filter(user_image_host = auth.get_user(request))[0].user_image_pass
    notes =  list(KNote.objects.filter(knote_host=auth.get_user(request).pk).order_by('-knote_date'))
    args['knotes'] = notes
    return render_to_response("user_page.html",args,context_instance=RequestContext(request))


def imgUpload(request):
    args = {}
    args.update(csrf(request))
    return render_to_response("test.html",args,context_instance=RequestContext(request))

def upload(request):
    args = {}
    args.update(csrf(request))
    for count,x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open(
                    "/home/vnavka/Documents/Dev/python/DB/Kursach/lincin/bin/courceLin/static/media/photo_"+str(auth.get_user(request).username+".png"),
                    "wb+") as destination:
                for chuck in f.chunks():
                    destination.write(chuck)

        process(x)

        image = UserImage.objects.filter(user_image_host = auth.get_user(request))[0]
        image.user_image_pass = str("/static/media/photo_"+str(auth.get_user(request).username+".png") )
        image.save()

    return redirect("/home/",context_instance = RequestContext(request))
    # return render_to_response("test.html",args,context_instance=RequestContext(request))

def add_knote(request):
    args = {}
    args['user_name'] = auth.get_user(request).username
    return render_to_response('notes_add.html',args,context_instance=RequestContext(request))



# def upload(request):
#     args = {}
#     args.update(csrf(request))
#     for count,x in enumerate(request.FILES.getlist("files")):
#         def process(f):
#             with open(
#                     "/static/media/photo.png",
#                     "wb+") as destination:
#                 for chuck in f.chunks():
#                     destination.write(chuck)
#
#         process(x)
#     return redirect("/home/")

def process_knote(request,knote_id = 1):
    args = {}
    args = request.POST
    note = KNote( knote_title = args["note_title"],
                  knote_note = args["note_main"],
                  knote_date = datetime.now(),
                  knote_views = 0,
                  knote_host = auth.get_user(request),)
    note.save()
    return redirect("/home/")

def process_knote_comment(request, knote_id = 1):
    args = {}
    args["note"] = KNote.objects.get(id = knote_id)
    args["note"].knote_views +=1;
    args["note"].save()
    args["comments"] = Comments.objects.filter(comment_note = knote_id)
    args['userimage'] = UserImage.objects.filter(user_image_host = KNote.objects.get(id = knote_id).knote_host)[0]

    return render_to_response("notes_view.html",args,context_instance = RequestContext(request))

def process_knote_del(request, knote_id = 1):
    note = KNote.objects.get(id = knote_id)
    Comments.objects.filter(comment_note = knote_id).delete()
    note.delete()
    return show_user(request)

def edit_knote(request, knote_id = 1):
    args={}
    args["note"]=KNote.objects.get(id = knote_id)
    return render_to_response("notes_edit.html",args,context_instance = RequestContext(request))


def edit_knote_save(request):

    args = {}
    args.update(csrf(request))
    if(request.method == "POST"):
        note_id = request.POST.get('note_id')
        note = KNote.objects.get(id = note_id)
        note.knote_title = request.POST['note_title']
        note.knote_note = request.POST['note_main']
        note.save()

    args['user_name'] = auth.get_user(request).username
    args['username'] = auth.get_user(request).username
    args['userimage'] = UserImage.objects.filter(user_image_host = auth.get_user(request))[0].user_image_pass
    notes =  list(KNote.objects.filter(knote_host=auth.get_user(request).pk).order_by('knote_date'))
    args['knotes'] = notes
    return redirect("/home/",context_instance = RequestContext(request))

def add_comment(request):


    args = {}
    args.update(csrf(request))
    if(request.method == "POST"):
        note_id = request.POST.get('note_id')
        comment = Comments(comment_login = auth.get_user(request).username,
                           comment_text = request.POST['comment_title'],
                           comment_note = KNote.objects.get(id = note_id)
                           )
        comment.save()
        way = str("/home/knote/" +str(note_id)+"/")
    return redirect("/home/",context_instance = RequestContext(request))

# def show_people(request):
#     args = {}
#     args["Users_reg"] = list(User.objects.filter()).__len__()
#     return render_to_response()



def dump_db(request):
    # settings.configure()
    # /home/vnavka/Documents/Dev/python/DB/Kursach/lincin/bin/courceLin/
    user = auth.get_user(request).is_superuser
    if(user):
        with open('reserve_copy.xml',"wt+") as f:
            call_command('dumpdata',format='xml',indent=4,stdout=f)
    return redirect("/")

def load_db(request):
    user = auth.get_user(request).is_superuser
    if(user):
        call_command('loaddata', 'reserve_copy.xml')
    return redirect("/")

def fill_db(request):
    word_base = [" Jack "," Ron "," Tonni "," Moker "," genster "," Dobrei"," asistant"," Gogo"," Allah"]
    for i in xrange(200):
        #print "User %s" %(i)
        name = str(word_base[randint(0,8)]+word_base[randint(0,8)])
        pasword = str(randint(1000,99999))
        mail = str(str(randint(1,99999)) + "@" + str(randint(1,99999)))
        user = User.objects.create_user(username=name,email=mail,password= pasword)
        user.save()
        image = UserImage(user_image_host = user).save()
        for j in xrange(100):
            note = KNote(knote_title = str(word_base[randint(0,8)]+word_base[randint(0,8)] + word_base[randint(0,8)]),
                              knote_note = str(word_base[randint(0,8)]+word_base[randint(0,8)]),
                              knote_date = datetime.now(),
                              knote_host = user)
            note.save()
            for k in xrange(10):
                comment = Comments(comment_text = str(word_base[randint(0,8)]+word_base[randint(0,8)]),
                                    comment_note = note,
                                    comment_login = "system").save()

    return redirect("/")

def show_users(request):
    lst = []
    people = User.objects.all()
    #print list(people).__len__()
    for i in people:
        image = UserImage.objects.filter(user_image_host = i)
        #print image
        if image.__len__() > 0:
             image=image[0]
        lst.append( [i,image.user_image_pass] )

    return render_to_response("people_view.html",{"data":lst})

def person_notes(request,person_id = 1):
    args ={}
    user = User.objects.get(id = person_id)
    args['user_name'] = user.username
    args['username'] = user.username
    args['userimage'] = UserImage.objects.filter(user_image_host = user)[0].user_image_pass
    notes =  list(KNote.objects.filter(knote_host=user).order_by('-knote_date'))
    args['knotes'] = notes
    return render_to_response("user_view.html",args,context_instance=RequestContext(request))

def show_knotes(request):
    data = []
    notes = KNote.objects.all().order_by('-knote_views')
    for note in notes:
        # print note.knote_host.id
        usr = User.objects.get(id = note.knote_host.id)
        picture = UserImage.objects.filter(user_image_host = usr)[0]
        data.append([note,usr,picture])
    return render_to_response("Knotes_view.html",{"data":data},context_instance=RequestContext(request))

def search_knotes(request):
    args = {}
    data = []
    args.update(csrf(request))
    if(request.method == "POST"):
        param = request.POST.get("text")
        #print param
        param = str(param)
        notes = KNote.objects.filter(knote_note__contains=param)
        for note in notes:
            usr = User.objects.get(id = note.knote_host.id)
            picture = UserImage.objects.filter(user_image_host = usr)[0]
            data.append([note,usr,picture])
    args["data"] = data
    return render_to_response("Knotes_view.html",{"data":data},context_instance=RequestContext(request))
