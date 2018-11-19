# rex.zhu
from django.db.models import Q

def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    #从GET 请求中获取过滤参数，重新组合成字典返回
    filter_conditions = {}
    # print("request.GET:",request.GET)
    keywords=['page',"o","_q"]
    for k,v in request.GET.items():
        if k in keywords:
            continue
        if v:
            filter_conditions[k] =v

    #根据过滤条件查询数据库
    return admin_class.model.objects.filter(**filter_conditions),filter_conditions

def table_sort(request,objs):
    orderby_key = request.GET.get("o")
    if orderby_key :
        res = objs.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key =  "-%s"%orderby_key
    else:
        return objs,""
    return res,orderby_key

def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))






def table_search(request,admin_class,object_list):
     search_key = request.GET.get("_q","")
     q_obj=Q()

     q_obj.connector="OR"

     for column in admin_class.search_fields :
         q_obj.children.append(("%s__contains"%column,search_key))

     res =  object_list.filter(q_obj)
     return res

    #  print("search:",search_key)
    #
    #
    # '''进行条件过滤并返回过滤后的数据'''
    # #从GET 请求中获取过滤参数，重新组合成字典返回
    # filter_conditions = {}
    #
    # # print("request.GET:",request.GET)
    # for k,v in request.GET.items():
    #     if k == "page" or k == "o" :
    #         continue
    #     elif k == "_q":
    #        q=Q(name__contains=v)
    #        continue
    #     if v:
    #         filter_conditions[k] =v
    #
    # #根据过滤条件查询数据库
    # print("search:",q)
    # print(admin_class.model.objects.filter(q))
    # return admin_class.model.objects.filter(q).filter(**filter_conditions)


