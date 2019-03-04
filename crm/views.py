from django.shortcuts import render,redirect,HttpResponse
from  king_admin import king_admin
# Create your views here.
from django.contrib.auth.decorators import login_required
from crm import models
from django.db import IntegrityError
import random,string
from crm import forms
from django.core.cache import cache
import os
from PerfectCRM import settings

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
                if enroll_obj.contract_agreed:  #判断学生是否已同意
                   return  redirect("/crm/contract_review/%s/"%enroll_obj.id)

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
        if request.is_ajax():   #保存上传文件
            print("ajax post : ", request.FILES)
            enroll_data_dir = "%s/%s"%(settings.ENROLLED_DATA,obj_id)
            if not os.path.exists(enroll_data_dir):  #判断目录是否存在
                os.makedirs(enroll_data_dir,exist_ok=True)
            for k,file_obj in request.FILES.items():  #保存文件
                with open("%s/%s"%(enroll_data_dir,file_obj.name),"wb") as f:
                    for chuck in file_obj.chunks():
                        f.write(chuck)

        customer_form = forms.CustomerForm(request.POST,instance=enroll_obj.customer)
        if customer_form.is_valid():
            customer_form.save()
            enroll_obj.contract_agreed =True
            enroll_obj.save()
            return render(request,"sales/stu_registration.html",{"status":1})
    else:
        customer_form = forms.CustomerForm(instance=enroll_obj.customer)

    return render(request,"sales/stu_registration.html",{"customer_form":customer_form,"enroll_obj":enroll_obj})



def contract_review(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    customer_form =  forms.CustomerForm(instance=enroll_obj.customer)
    enroll_form = forms.EnrollmentForm(instance=enroll_obj)

    return  render(request,"sales/contract_review.html",{"enroll_obj":enroll_obj,"customer_form":customer_form,"enroll_form":enroll_form})



def enrollment_rejection(request,enroll_id):
    enroll_obj =  models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_agreed=False
    enroll_obj.save()
    return redirect("/crm/customers/%s/enrollment/"%enroll_obj.customer.id)



def payment(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    errors=[]
    print(enroll_obj)
    if request.method == "POST":
        payment_amount =  request.POST.get("amount")
        if payment_amount:
            payment_amount = int(payment_amount)
            if payment_amount < 500 :
                errors.append("缴费金额不能低于500")
            else:
                payment_obj = models.Payment.objects.create(
                    customer= enroll_obj,
                    course =  enroll_obj.enrollment_class.course,
                    amount= payment_amount,
                    consultant= enroll_obj.consultant
                )
                enroll_obj.customer.status = 0
                enroll_obj.customer.save()
                return  redirect("/king_admin/crm/customer/")

    if  not enroll_obj.contract_approved:
        enroll_obj.contract_approved =True
        enroll_obj.save()


    return render(request,"sales/payment.html",{"enroll_obj":enroll_obj,"errors":errors})