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
    user=f.getUser(request.COOKIES.get("userName"))
    q['uID']=user['uID']
    q['type']=user['type']
    q['question']=request.GET['askedQuestion']
    q['votes']={}
    q['answers']=[]
    q['subject']=request.GET['subject']
    if f.addQuestion(q):
        questions = f.getQuestions()
        return render(request, 'mainapp/forum.html',{"questions":questions})
    return render(request, 'mainapp/forum1.html',{})

def index(request):
    if request.COOKIES.get("loggedIn", None):
        return render(request, 'mainapp/forum.html', {'questions':Forum().getQuestions()})
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
        msg="u are not logged in to log out"
        render(request, 'mainapp/forum1.html', {'msg':msg})

def register(request):
    import random
    uId=request.GET['uID']
    email=request.GET['email']
    otp= random.randint(1000,9999)
    sendMail(email,otp)
    ctx={"uId":uId,"email":email, "otp":otp}
    response = render(request, 'mainapp/r_validate.html', {"ctx":ctx})
    response.set_cookie("uidReg", uId)
    response.set_cookie("emailReg", email)
    response.set_cookie("otp", otp)
    return response

def r_validate(request):
    uID=request.COOKIES.get("uidReg")
    email=request.COOKIES.get("emailReg")
    password=request.GET['pass']
    type=request.GET['type']

    uotp=request.GET['uotp']
    otp=request.COOKIES.get("otp")
    if otp==uotp:
        f=Forum()
        f.addUser({"uID":uID, "type":type, "email":email, "password":password, "aura":0, "qAsked":[]})
        response =render(request, 'mainapp/login.html', {})
        response.delete_cookie("uidReg")
        response.delete_cookie("emailReg")
        response.delete_cookie("otp")
        response.delete_cookie("qID")
        return response
    else:
        msg="otp doesnt match"
        render(request, 'mainapp/forum1.html', {'msg':msg})


def getQuestionDetails(request,qID):
    question = Forum().getAnswers(int(qID))
    response= render(request,'mainapp/answer.html',{'question':question})
    response.set_cookie('qID',qID)
    return response

def sendMail(email,otp):
    '''sends mail provided email and otp'''
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("apnnarayana@gmail.com", "aappnnaassss")
    message = "welcome to cvr forum\n\nyout otp is:"+str(otp)
    s.sendmail("apnnarayana@gmail.com", email, message)
    s.quit()

def postAnswer(request):
    qID=request.COOKIES.get("qID")
    answer={}
    f=Forum()
    user = f.getUser(request.COOKIES.get("userName"))
    answer['type']=user['type']
    answer['uID']=user['uID']
    answer['answer']=request.GET['answeredAnswer']
    answer['votes']={}
    f.addAnswer(qID,answer)
    return getQuestionDetails(request,qID)