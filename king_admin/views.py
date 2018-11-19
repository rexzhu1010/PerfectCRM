from django.shortcuts import render
import importlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import  table_filter,prn_obj,table_sort,table_search
# Create your views here.
from king_admin import king_admin
from crm import models

def index(request):
    #print(king_admin.enabled_admins['crm']['customerfollowup'].model )
    # print(king_admin.enable_admins)
    # prn_obj(king_admin.enable_admins['crm']['customer'])
    # print("11111111111")
    # print(dir(models.Customer._meta))
    # print("11111111111")
    return render(request, "king_admin/table_index.html",{'table_list':king_admin.enable_admins})


def display_table_objs(request,app_name,table_name):

    request.GET

    print("-->",app_name,table_name)
    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    admin_class = king_admin.enable_admins[app_name][table_name]
    #admin_class = king_admin.enabled_admins[crm][userprofile]
    prn_obj(admin_class)

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
                                                         "search_q":request.GET.get("_q") or ""},
                                                        )