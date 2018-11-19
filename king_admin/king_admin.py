# rex.zhu


from crm import models

enable_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 5



class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','consult_course','date','status']
    list_filters = ['source','consultant','consult_course','status',"qq"]
    search_fields = ['qq',"name","consultant__name"]    # consultant 是外键 要按名字搜索 要 __name
    #model = models.Customer


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer','consultant','date')

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] =  admin_class



register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)