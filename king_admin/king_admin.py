# rex.zhu


from crm import models

from django.shortcuts import redirect,render

enable_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 5
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_objs",]


    def delete_selected_objs(self,request,querysets):


        if request.POST.get("delete_confirm")=="yes":
            querysets.delete()
            return  redirect("/king_admin/%s/%s"%(self.model._meta.app_label,self.model._meta.model_name))
        print("delete_selected_objs",self,request,querysets)

        selected_ids = ','.join([str(i.id) for i in querysets])
        print("request._admin_action",request._admin_action)
        print("这是要删除的 selected_ids",selected_ids)
        return render(request,"king_admin/table_obj_delete.html",{"objs":querysets,
                                                                  "admin_class":self,
                                                                  "app_name":self.model._meta.app_label,
                                                                  "table_name":self.model._meta.model_name,
                                                                  "selected_ids":selected_ids,
                                                                  "action":request._admin_action
                                                                  })



class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','status']
    list_filters = ['source','consultant','consult_course','status',"qq","date"]
    search_fields = ['qq',"name","consultant__name"]    # consultant 是外键 要按名字搜索 要 __name
    filter_horizontal = ['tags',]
    #model = models.Customer
    ordering = "-date"

    readonly_fields = ["qq", "consultant"]

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ("id",'customer','consultant','date')

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] =  admin_class


class UserProfileAdmin(BaseAdmin):
    list_display = ("user","name")

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserProfileAdmin)