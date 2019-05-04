from django.shortcuts import render
from .models import Forum
# Create your views here.
def forum():
    f = Forum()
    questions=f.getQuestions()
    return questions

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

def index(request):
    if request.COOKIES.get("loggedIn", None):
        return render(request, 'mainapp/forum.html', {})

    return render(request, 'mainapp/login.html', {})

def login(request):
    uID = request.GET['logUser']
    psw =request.GET['logPass']
    f=Forum()
    user = f.getUser(uID)
    if user and user['password']==psw:
        questions= forum()
        response = render(request, 'mainapp/forum.html', {'questions': questions})
        response.set_cookie("loggedIn", True)
        response.set_cookie("userName", uID)
        return response
    else:
        return render(request,'mainapp/forum1.html',{})
def logout(request):
    if request.COOKIES.get("loggedIn"):
        response =  render(request, 'mainapp/login.html', {})
        response.delete_cookie("userName")
        response.delete_cookie("loggedIn")
        return response
    else:
        render(request, 'mainapp/forum1.html', {})

def register(request):
    uId=request.GET['uID']
    email=request.GET['email']
    ctx={"uId":uId,"email":email}
    return render(request, 'mainapp/forum.html', {"ctx":ctx})

def r_validate(request):
    return render(request,'mainapp/forum.html',{})



def sendMail(email,otp):
    '''sends mail provided email and otp'''
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("apnnarayana@gmail.com", "aappnnaassss")
    message = "welcome to cvr forum\n\nyout otp is:"+otp
    s.sendmail("apnnarayana@gmail.com", email, message)
    s.quit()

