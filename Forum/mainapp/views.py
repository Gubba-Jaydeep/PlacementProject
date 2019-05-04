from django.shortcuts import render
from .models import Forum
# Create your views here.
def forum(request):
    f = Forum()
    questions=f.getQuestions()
    return render(request, 'mainapp/forum.html',{"questions":questions})

def askQuestion(request):
    f = Forum()
    #newQuestion
    q={}
    q['name']=request.GET['name']

    f.addQuestion(q)
    questions = f.getQuestions()
    return render(request, 'mainapp/forum.html',{"questions":questions})
