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
    q['uID']='16B81A05B8'
    q['type']='student'
    q['question']=request.GET['askedQuestion']
    q['votes']=0
    q['answers']=[]
    q['subject']=request.GET['subject']

    if f.addQuestion(q):
        questions = f.getQuestions()
        return render(request, 'mainapp/forum.html',{"questions":questions})
    return render(request, 'mainapp/forum1.html',{})

def login(request):
    f=Forum()
    uID=12
    users=f.getUser(uID)
    return render(request,'mainapp/forum.html',{})

def register(request):
    return render(request, 'mainapp/forum.html', {})

def r_validate(request):
    return render(request,'mainapp/forum.html',{})

def logout(request):
    return render(request, 'mainapp/forum.html', {})

def sendMail(email,otp):
    '''sends mail provided email and otp'''
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("apnnarayana@gmail.com", "aappnnaassss")
    message = "welcome to cvr forum\n\nyout otp is:"+otp
    s.sendmail("apnnarayana@gmail.com", email, message)
    s.quit()

