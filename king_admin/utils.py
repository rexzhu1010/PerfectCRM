# rex.zhu


def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    #从GET 请求中获取过滤参数，重新组合成字典返回
    filter_conditions = {}
    print("request.GET:",request.GET)
    for k,v in request.GET.items():
        if k == "page" or k == "o":
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
