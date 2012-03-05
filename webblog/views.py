# Create your views here.
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from webblog.models import *
from webblog.forms import *

MESSAGES = {'edit_success'     : 'Blogpost erfolgreich editiert.',
            'delete_success'   : 'Blogpost erfolgreich geloescht.',
            'create_success'   : 'Blogpost erfolgreich erstellt',
            'login_success'    : 'Erfolgreich eingeloggt.',
            'register_sccuess' : 'Benutzer erfolgreich erstellt.',
            'logout_success'   : 'Erfolgreich ausgeloggt'}

def index(request, postnumber = 1):
    postnumber = int(postnumber)
    postnumber -= 1                                                                                                 #postnr zu listindex
    blogposts = Blogpost.objects.all()
    blogposts =  blogposts if postnumber in range(0,len(blogposts)) else []                                            #ersten Index pruefen
    if blogposts:
        showposts = blogposts[postnumber:(postnumber+15 if postnumber+15 <= len(blogposts) else len(blogposts))]    #zweiten Index pruefen
    else:
        showposts = []                                                                                              #keine Posts unter postnr
    likes = {}
    for i in range(0,len(showposts)-1):
        likes[showposts[i].pk] = len(showposts[i].likes.all())
    return render_to_response('index.html',{'blogposts' : showposts, 'message' : MESSAGES.get(request.GET.get('msg',''),''),
                              'likes' : likes}, context_instance=RequestContext(request))

def redirect_index(request):
    return HttpResponseRedirect('/index/post=1')

def login(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user = auth.authenticate(username=user_name,password=user_password)
            if user != None and user.is_active:
                auth.login(request,user)

                return HttpResponseRedirect(request.GET.get('next','/index/post=1/?msg=login_success'))
            else:
                errors.append('Benutzer oder Password nicht bekannt.')
        return render_to_response('user/login.html', {'form' : form, 'errors' : errors}, context_instance=RequestContext(request))

    else:
        form = LoginForm()
        return render_to_response('user/login.html', {'form' : form, 'errors' : errors}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']
            user = auth.authenticate(username=user_name,password=user_password)
            auth.login(request,user)
            return HttpResponseRedirect(request.GET.get('next','/index/post=1/?msg=register_sccuess'))
        else:
            return render_to_response('user/register.html', {'form' : form},context_instance=RequestContext(request))
    else:
        form = UserCreationForm()
        return render_to_response('user/register.html', {'form' : form},context_instance=RequestContext(request))

@login_required()
def create_blogpost(request):
    if request.method == 'POST':
        form = BlogpostCreationForm(request.POST)
        if form.is_valid():
            blogpost = Blogpost(author = request.user,
                                content = form.cleaned_data['post_content'],
                                publication_date = datetime.datetime.now(),
                                title = form.cleaned_data['post_title'],
                                tags = form.cleaned_data['post_tags'])
            blogpost.save()
            return HttpResponseRedirect('/index/post=1/?msg=%s' % 'create_success')
        else:
            return render_to_response('post/create_blogpost.html', {'form' : form},context_instance=RequestContext(request))
    else:
        form = BlogpostCreationForm()
        return render_to_response('post/create_blogpost.html', {'form' : form},context_instance=RequestContext(request))

@login_required()
def edit_blogpost(request, postid):
    post = Blogpost.objects.get(pk=postid)

    if post == None:
        raise Http404

    if not edit_delete_permission(request, post):
        return HttpResponse('403 Forbidden')

    if request.method == 'POST':
        form = BlogpostCreationForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['post_title']
            post.content = form.cleaned_data['post_content']
            post.tags = form.cleaned_data['post_tags']
            post.save()
            return HttpResponseRedirect('/blogpost/detail/id=%s/?msg=%s' % (postid, 'edit_success'))
        else:
            return render_to_response('post/edit_blogpost.html', {'form' : form},context_instance=RequestContext(request))
    else:
        form = BlogpostCreationForm(initial={'post_title' : post.title, 'post_content' : post.content, 'post_tags' : post.tags})
        return render_to_response('post/edit_blogpost.html', {'form' : form},context_instance=RequestContext(request))


@login_required()
def delete_blogpost(request, postid):
    post = Blogpost.objects.get(pk=postid)

    if post == None:
        raise Http404

    if not edit_delete_permission(request, post):
        return HttpResponse('403 Forbidden')

    if request.method == 'POST':
        if 'delete_confirm' in request.POST:
            post.delete()
            return HttpResponseRedirect('/index/post=1/?msg=%s' % 'delete_success')

        else:
            return HttpResponseRedirect('/index/post=1')
    else:
        return render_to_response('post/delete_blogpost.html', {'blogpost':post},context_instance=RequestContext(request))


@login_required()
def detail_blogpost(request, postid):
    post = Blogpost.objects.get(pk=postid)

    if post == None:
        raise Http404

    comments = Comment.objects.all().filter(blogpost = post)


    return render_to_response('post/detail_blogpost.html', {'blogpost' : post,
                                                            'comments' : comments,
                                                            'message' : MESSAGES.get(request.GET.get('msg',''),'')},
                                                             context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/post=1/?msg=%s' % 'logout_success')


def edit_delete_permission(request, post):
    if not (request.user == post.author or request.user.is_superuser == 1):
        return False
    else:
        return True


