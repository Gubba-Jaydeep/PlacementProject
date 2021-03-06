from django.shortcuts import render
from .models import Forum
# Create your views here.
def forum():
    f = Forum()
    questions=f.getQuestions()
    return reversed(questions)

def askQuestion(request):
    f = Forum()
    #newQuestion
    q={}
    user=f.getUser(request.COOKIES.get("userName"))
    q['uID']=user['uID']
    q['type']=user['type']
    q['question']=request.GET['askedQuestion']
    q['votes']={'yes':[],'no':[]}
    q['answers']=[]
    q['subject']=request.GET['subject']
    if f.addQuestion(q):
        questions = f.getQuestions()
        questions.reverse()
        return render(request, 'mainapp/forum.html',{"questions":questions})
    return render(request, 'mainapp/forum1.html',{})

def index(request):
    if request.COOKIES.get("loggedIn", None):
        return render(request, 'mainapp/forum.html', {'questions':reversed(Forum().getQuestions())})
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
    u_name=request.GET['u_name']
    uotp=request.GET['uotp']
    otp=request.COOKIES.get("otp")
    if otp==uotp:
        f=Forum()
        f.addUser({"uID":uID,"u_name":u_name , "type":type, "email":email, "password":password, "aura":0, "qAsked":[]})
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
    answer['votes']={'yes':[],'no':[]}
    f.addAnswer(qID,answer)
    return getQuestionDetails(request,qID)

def incQuestionVote(request):
    qID=request.COOKIES.get('qID')
    Forum().questionVote(request.COOKIES.get('userName'),int(qID),'yes')
    return getQuestionDetails(request, qID)

def decQuestionVote(request):
    qID=request.COOKIES.get('qID')
    Forum().questionVote(request.COOKIES.get('userName'),int(qID),'no')
    return getQuestionDetails(request, qID)

def incAnswerVote(request,aID):
    qID = request.COOKIES.get('qID')
    Forum().answerVote(request.COOKIES.get('userName'),int(aID), int(qID), 'yes')
    return getQuestionDetails(request,qID)

def decAnswerVote(request,aID):
    qID = request.COOKIES.get('qID')
    Forum().answerVote(request.COOKIES.get('userName'),int(aID), int(qID), 'no')
    return getQuestionDetails(request,qID)

def profile(request):
    user = Forum().getUser(str(request.COOKIES.get('userName')))
    return render(request, 'mainapp/profile.html', {'user': user})

def info(request):
    #we should create another collection of information which contains all messages(info) sent by all teachers..
    #so single db object is sufficient with array of msgs(each with userameof teacher(not anonymous),date,text,img=none(default) etc)
    user = Forum().getUser(str(request.COOKIES.get('userName')))
    msgs = Forum().getMssg()
    if user['type']=="teacher":
        return render(request, 'mainapp/info.html', {'user': user,'type':user['type'],'msgs':msgs})
    return render(request,'mainapp/info.html',{'msgs':msgs})


def addData(request):
    msgText = request.GET['msgText']
    user = Forum().getUser(str(request.COOKIES.get('userName')))
    uname=user['u_name']
    Forum().addMsg(msgText,uname)
    msgs = Forum().getMssg()
    return render(request, 'mainapp/info.html', {'user': user, 'type': user['type'], 'msgs': msgs})
