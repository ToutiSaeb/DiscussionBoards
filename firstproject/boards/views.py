import http.client

from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from  django.contrib.auth.models import User
from  .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
def home(request):
    boards=Board.objects.all()
    return render(request,'home.html',{'boards':boards})
def board_topics(request,board_id):
    try:
      board=Board.objects.get(pk=board_id)
    except:
        raise Http404
    print("-----------------------")
    print(board)
    return render(request, 'topics.html', {'board': board})
 #topic=get_list_or_404(Board,pk=board_id)


''' board_names=[]
    for element in board:
        board_names.append(element.name)
    response_html='<br>'.join(board_names)
    return HttpResponse(response_html)'''
@login_required

def new_topic(request,board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except:
        raise Http404
    '''  forms html simple
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        user=User.objects.first()
        topic=Topic.objects.create(
            subject=subject,
            board=board,
            created_by=user
        )
        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )
        return  redirect('board_topics',board_id=board.pk)
        print(subject,message)'''
    #forms of django
    #user = User.objects.first()
    if request.method == 'POST':
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic = form.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', board_id=board.pk)
    else:
        form = NewTopicForm()

    return render(request,'new_topic.html',{'board': board,'form':form})

def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    return render(request,'topic_posts.html',{'topic':topic})
@login_required
def reply_topic(request, board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            return redirect('topic_posts',board_id=board_id, topic_id = topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})





# Create your views here.
