from django.shortcuts import render
from account.models import *
from rest_framework.response import Response
from django.db.models import Sum

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        if User.objects.filter(username=username).count()<1:
            u = User(username=username,email=email)
            u.set_password(password)
            u.save()
            f = FulfillUser(user=u)
            f.save()
            return Response({'status':'okay'},status=200)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return Response({'status':'ok'},status=200)
        return Response({'status':'user not exist'},status=404)


def make_task(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        difficulty = request.POST.get('difficulty', '')
        category = request.POST.get('category', '')
        due_date = request.POST.get('due_date', '')
        done_progress = request.POST.get('done_progress', '')
        score = request.POST.get('score', '')
        if Category.objects.filter(name=category).count() < 1:
            c = Category(name=category)
            c.save()
        else:
            c = Category.objects.get(name=category)
        f = FulfillUser.objects.get(user=User.objects.get(username=username))
        t = Task(title=title, description=description, difficulty=difficulty, category=c,
                 due_date=due_date, done_progress=done_progress, score=score, user=f)
        t.save()

def categories_rank(request):
    t = Task.objects.values('category').annotate(Sum('score'))[0]
    return Response(t)


def user_score(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        u = User.objects.get(username=username)
        f = FulfillUser.get(user=u)
        result = Task.objects.filter(user=f).aggregate(Sum('score'))
        return Response(result)


def user_rank(request):
    if request.method == 'GET':
        username = request.GET.get('username','')
        result = []
        for j in Category.objects.all():
            rankings = Task.objects.filter(category=j).values('user').annotate(Sum('score'))
            result.append(rankings)
        return Response(result)


def first_scores(request):
    if request.method == 'GET':
        result = {}
        for i in FulfillUser.objects.all():
            result[i.user.username] = 0
            for j in Task.objects.all():
                if j.user == i:
                    result[i.user.username] += j.score
        print(result)


def reset_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        FulfillUser.objects.get(user=User.objects.get(username=username)).delete()
        User.objects.get(username=username).delete()
        return Response({'status':'ok'})    
