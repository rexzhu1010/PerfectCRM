# rex.zhu

from django.shortcuts import redirect


#这个是息定义钩子权限 ，可动态判断url的get或post传参， 比如限制 consultant 必须等于 登入的ID 号
def  view_my_own_coustomer(request,permission_val):
    print("running the permission_hook !!!!!!!!!!!!!!!!!!")
    my_url=""
    print(permission_val[2],request.GET,request.user.id)
    if permission_val[2] and not request.GET:

        for var in  permission_val[2]:
            my_arg=""
            if var == "consultant":
                my_arg=request.user.id
            my_url += "%s=%s"%(var,my_arg)
        print("这是要跳的URL %s?%s"%(request.path,my_url))
        return  redirect("%s?%s"%(request.path,my_url))

    # if request.user
    print("看看GET 有没有参数： ",request.GET)
    return True