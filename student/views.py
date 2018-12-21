from django.shortcuts import render

# Create your views here.
from crm import models

def stu_my_classes(requet):
    return render(requet,"student/my_classes.html",{})


def  studyrecords(request,):
    return  render(request,"student/studyrecords.html")
