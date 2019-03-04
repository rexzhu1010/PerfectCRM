from django.shortcuts import render,redirect
import importlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import  table_filter,prn_obj,table_sort,table_search
# Create your views here.
from king_admin import king_admin,forms
from crm import models
from django.contrib.auth.decorators import login_required

from king_admin import permission,permission_list


@permission.check_permission
@login_required
def index(request):
    #print(king_admin.enabled_admins['crm']['customerfollowup'].model )
    # print(king_admin.enable_admins)
    # prn_obj(king_admin.enable_admins['crm']['customer'])
    # print("11111111111")
    # print(dir(models.Customer._meta))
    # print("11111111111")
    return render(request, "king_admin/table_index.html",{'table_list':king_admin.enable_admins})


@permission.check_permission
@login_required
def display_table_objs(request,app_name,table_name):

    print("-->",app_name,table_name)
    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    admin_class = king_admin.enable_admins[app_name][table_name]
    #admin_class = king_admin.enabled_admins[crm][userprofile]
    if request.method ==  "POST" :
        print("操作 action",request.POST.get("action"))
        selected_ids = request.POST.get("selected_ids")
        if selected_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(","))
        else:
            raise KeyError("No object selected")
        action = request.POST.get("action")

        if hasattr(admin_class,action):
            action_func = getattr(admin_class,action)
            request._admin_action = action
            return action_func(admin_class,request,selected_objs)


    #object_list = admin_class.model.objects.all()
    object_list,filter_condtions = table_filter(request,admin_class)


    object_list  = table_search(request,admin_class,object_list)

    object_list,orderby_key= table_sort(request,object_list)


    # print("object:",object_list)


    paginator = Paginator(object_list, admin_class.list_per_page) # Show 25 contacts per page

    page = request.GET.get('page')

    # print("PAGE:",page)
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    # print("views.filter_condtions:",filter_condtions)
    # print(222222222222222)
    # #print(list(query_sets)[0])
    # # prn_obj(list(query_sets)[0])
    # # print(query_sets.has_previous)
    # print("222222222222222222222222222222",query_sets.paginator.page_range,"333333333333333333333333333")
    return render(request,"king_admin/table_objs.html",{"admin_class":admin_class,
                                                        "query_sets":query_sets,
                                                        "filter_condtions":filter_condtions,
                                                        "orderby_key":orderby_key,
                                                        "previous_orderby":request.GET.get("o") or "",
                                                         "search_q":request.GET.get("_q") or "",
                                                         "selectdate":request.GET.get("date") or ""},
                                                        )

@permission.check_permission
@login_required
def table_objs_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enable_admins[app_name][table_name]
    admin_class.is_add_form = False
    model_form_class =  forms.create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj=model_form_class(request.POST,instance=obj) # 把新POST，和旧的OBJ 都交给 modelform 对比 才是更新
        #orm_obj = model_form_class(request.POST) #这不是更新，这是增加

        if form_obj.is_valid():
            print("保存前 cleaned_data:",form_obj.cleaned_data)
            form_obj.save()
            return redirect("/king_admin/%s/%s/" % (app_name, table_name))

    else:
        form_obj= model_form_class(instance=obj)
    return  render(request,"king_admin/table_obj_change.html",{"form_obj":form_obj,"admin_class":admin_class,"app_name":app_name,"table_name":table_name})



@permission.check_permission
@login_required
def table_objs_add(request,app_name,table_name):
    print("add")
    admin_class = king_admin.enable_admins[app_name][table_name]
    admin_class.is_add_form =  True
    model_form_class =  forms.create_model_form(request,admin_class)


    if request.method == "POST":

        form_obj=model_form_class(request.POST) # 把新POST，和旧的OBJ 都交给 modelform 对比 才是更新


        if form_obj.is_valid():
            print("form表单验证成功后",form_obj)
            form_obj.save()
            print("添加成功")
            return redirect(request.path.replace("/add/","/"))
        else:
            model_form_class = form_obj

    return  render(request,"king_admin/table_obj_add.html",{"form_obj":model_form_class,"admin_class":admin_class,})


@permission.check_permission
@login_required
def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class =  king_admin.enable_admins[app_name][table_name]
    # model_form_class  = forms.create_model_form(request,admin_class)
    obj =  admin_class.model.objects.get(id=obj_id)
    objs = [obj,]
    errors={}
    if admin_class.readonly_table:
        # 如该表是只读
        errors = {"readonly_table": "table is readonly [%s] cat not be delete" % table_name}
    else:
        errors={}
    if request.method == "POST":
        if not admin_class.readonly_table:
            obj.delete()
            return redirect("/king_admin/%s/%s/"%(app_name,table_name))



    return  render(request,"king_admin/table_obj_delete.html",{"objs":objs,"app_name":app_name,"table_name":table_name,"errors":errors})


@permission.check_permission
@login_required
def password_reset(request,app_name,table_name,obj_id):
    admin_class =  king_admin.enable_admins[app_name][table_name]
    obj =  admin_class.model.objects.get(id=obj_id)
    errors = {}
    if request.method == "POST":
        _password1 =  request.POST.get("password1")
        _password2 =  request.POST.get("password2")

        if _password1 == _password2 :
            if len(_password2) > 5:
                obj.set_password(_password1)
                obj.save()
                print("1111111111111111",request.path.rstrip("password/"))
                return redirect(request.path.rstrip("password/"))
            else:
                errors['ivalid_password'] = "must not less 6 letters"
        else:
            errors['ivvalid_password'] = 'passowrds are not the same'


    return render(request,"king_admin/password_reset.html",{"obj":obj,"errors":errors})



