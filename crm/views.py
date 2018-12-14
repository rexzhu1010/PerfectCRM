from django.shortcuts import render,redirect,HttpResponse
from  king_admin import king_admin
# Create your views here.
from django.contrib.auth.decorators import login_required
from crm import models
from django.db import IntegrityError
import random,string
from crm import forms
from django.core.cache import cache

@login_required
def index(request):
    print("我是crm ...........................")

    return render(request,"index.html")

@login_required
def customer_list(request):
    return render(request,"sales/customers.html")




@login_required
def enrollment(request,obj_id):
    customer_obj = models.Customer.objects.get(id=obj_id)
    msgs = {}

    if request.method == "POST":
        enroll_form = forms.EnrollmentForm(request.POST)
        if enroll_form.is_valid():

            try :
                enroll_form.cleaned_data["customer"]=customer_obj
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
            except  IntegrityError as e :
                enroll_form.add_error("__all__","该用户的此条报名信息已存在，不能重复报名！！！")
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrollment_class_id=enroll_form.cleaned_data[
                                                               "enrollment_class"].id)

            # msgs["register_link"].fomat(enroll_obj_id=enroll_obj.id,random_str=random_str)
            random_str =  "".join(random.sample(string.ascii_lowercase+string.digits,8))
            cache.set(enroll_obj.id,random_str,3000)
            msgs["register_link"] = "请将此链接复制给客户 \n  http://127.0.0.1:8000/crm/customers/stu_registration/%s/%s/"%(enroll_obj.id,random_str)

    else:
        enroll_form  = forms.EnrollmentForm()

    return  render(request,"sales/enrollment.html",{"enroll_form":enroll_form,"customer_obj":customer_obj,"msgs":msgs})



def  student_registration(request,obj_id,random_str):

    if cache.get(obj_id) != random_str:
        return HttpResponse("链接已失效！！！！！！！！！！！！！！！%s %s"%(cache.get(obj_id),random_str))
    enroll_obj =  models.Enrollment.objects.get(id=obj_id)
    if enroll_obj.contract_agreed :
        return render(request, "sales/stu_registration.html", {"status": 1})
    if request.method=="POST":
        customer_form = forms.CustomerForm(request.POST,instance=enroll_obj.customer)
        if customer_form.is_valid():
            customer_form.save()
            enroll_obj.contract_agreed =True
            enroll_obj.save()
            return render(request,"sales/stu_registration.html",{"status":1})
    else:
        customer_form = forms.CustomerForm(instance=enroll_obj.customer)

    return render(request,"sales/stu_registration.html",{"customer_form":customer_form,"enroll_obj":enroll_obj})
