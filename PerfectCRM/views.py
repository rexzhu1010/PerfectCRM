from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import login,authenticate,logout

def acc_login(requet):
    errors={}
    if requet.method == "POST":
        _email =  requet.POST.get("email")
        _password = requet.POST.get("password")
        user =  authenticate(username=_email,password= _password)#如果验证成功就返回用户对象，不成功就是None
        if user:
            login(requet,user)
            return redirect("/")
        else:
            errors["error"] = "Wrong username or password!"


    return render(requet,"login.html",{"errors":errors})


def acc_logout(request):
    logout(request)
    return redirect("/accounts/login/")

