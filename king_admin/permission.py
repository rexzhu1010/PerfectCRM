#__author:  Administrator
#date:  2017/1/19
from django.shortcuts import  HttpResponse,render,redirect

from django.urls import resolve

from  king_admin import permission_list

# def perm_check(*args,**kwargs):
#     request= args[0]
#     print("request path:",request.path )
#     if request.user.is_authenticated:
#         for permission_name, v in permission_list.perm_dic.items():
#             print(permission_name, v)
#             url_matched =  False
#             if v['url_type'] == 1: #absolute
#                 if v['url'] == request.path: #绝对url匹配上了
#                     url_matched = True
#             else:
#                 #把绝对的url请求转成相对的url name
#                 resolve_url_obj = resolve(request.path)
#                 print('resolve_url_obj',resolve_url_obj)
#                 if resolve_url_obj.url_name == v['url']:#相对的url 别名匹配上了
#                     url_matched = True
#
#             if url_matched:
#                 print("url  matched...")
#                 if v['method'] == request.method: #请求方法也匹配上了
#                     arg_matched = True
#                     for request_arg in v['args']:
#                         request_method_func = getattr(request,v['method'])
#                         if not request_method_func.get(request_arg):
#                             arg_matched = False
#
#                     if arg_matched:#走到这里，仅代表这个请求 和这条权限的定义规则 匹配上了
#                         print("arg  matched...")
#                         if request.user.has_perm(permission_name):
#                             #有权限
#                             print("有权限",permission_name)
#                             return True
#
#
#     else:
#         return redirect("/account/login/")


# def check_permission(func):
#     print('--------check_permission')
#     def inner(*args,**kwargs):
#         print("--permission:",*args,**kwargs)
#         print("--func:",func)
#         if perm_check(*args,**kwargs) is True:
#             return func(*args,**kwargs)
#         else:
#             return HttpResponse("没权限")
#     return inner


from django.urls import resolve
from django.shortcuts import render,redirect,HttpResponse
from king_admin.permission_list import perm_dic
from django.conf import settings


def perm_check(*args,**kwargs):

    request = args[0]
    print("111111111111",request.path)
    resolve_url_obj = resolve(request.path)  # 转成  urls 中定义的name
    current_url_name = resolve_url_obj.url_name  # 当前url的url_name
    print("current_url_name",current_url_name)
    print('---perm:',request.user,request.user.is_authenticated,current_url_name)
    #match_flag = False
    match_key = None
    match_results = [None,]
    if request.user.is_authenticated  is False:
         return redirect(settings.LOGIN_URL)

    for permission_key,permission_val in  perm_dic.items():

        per_url_name = permission_val[0]
        per_method  = permission_val[1]
        perm_args = permission_val[2]
        perm_kwargs = permission_val[3]
        perm_hook_func = permission_val[4] if len(permission_val)>4 else None

        perm_hook_matched = True
        if perm_hook_func:
            perm_hook_matched =  perm_hook_func(request,permission_val)
            print(perm_hook_matched)



        if per_url_name == current_url_name: #matches current request url
            if per_method == request.method: #matches request method
                # if not  perm_args: #if no args defined in perm dic, then set this request to passed perm

                #逐个匹配参数，看每个参数时候都能对应的上。
                args_matched = False #for args only
                for item in perm_args:
                    request_method_func = getattr(request,per_method)  #反射拿GET or PORT 过来的所有数据
                    if request_method_func.get(item,None):# request字典中有此参数
                        args_matched = True
                    else:
                        print("arg not match......")
                        args_matched = False
                        break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:  #完全匹配完，或列表为空执行
                    args_matched = True
                #匹配有特定值的参数
                kwargs_matched = False
                for k,v in perm_kwargs.items():
                    request_method_func = getattr(request, per_method)
                    arg_val = request_method_func.get(k, None)  # request字典中有此参数
                    print("perm kwargs check:",arg_val,type(arg_val),v,type(v))
                    if arg_val == str(v): #匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=3的参数
                        kwargs_matched = True
                    else:
                        kwargs_matched = False
                        break # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:
                    kwargs_matched = True



                match_results = [args_matched,kwargs_matched,perm_hook_matched]
                print("--->match_results ", match_results)
                if all(match_results): #都匹配上了
                    match_key = permission_key
                    break




    if all(match_results):
        app_name, *per_name = match_key.split('_')    # k="a_b_c"    k1,*k2 = k.split("_")    k1=a, k2=bc
        print("--->matched ",match_results,match_key)
        print(app_name, *per_name)
        perm_obj = '%s.%s' % (app_name,match_key)
        print("perm str:",perm_obj)
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False

    else:
        print("未匹配到权限项，当前用户无权限")




def check_permission(func):
    def inner(*args,**kwargs):
        if perm_check(*args,**kwargs) is True:
            return func(*args,**kwargs)
        else :
            return func(*args, **kwargs)
            #return HttpResponse("木有权限！！！")
    return inner