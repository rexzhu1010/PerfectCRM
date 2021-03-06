# rex.zhu


from crm import models

from django.shortcuts import redirect,render

from django.forms import  ValidationError
from  django.utils.translation import  ugettext as _
from django.shortcuts import render,redirect,HttpResponse

enable_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 5
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_objs", ]
    readonly_table = False
    readonly_fields = []
    form_exclude_field = ()

    def delete_selected_objs(self, request, querysets):
        if self.readonly_table:
            # 如该表是只读
            errors = {"readonly_table": "This table is readonly  cat not be delete" }
        else:
            errors = {}
        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
                return redirect("/king_admin/%s/%s" % (self.model._meta.app_label, self.model._meta.model_name))
        print("delete_selected_objs", self, request, querysets)

        selected_ids = ','.join([str(i.id) for i in querysets])
        print("request._admin_action", request._admin_action)
        print("这是要删除的 selected_ids", selected_ids)
        return render(request, "king_admin/table_obj_delete.html", {"objs": querysets,
                                                                    "admin_class": self,
                                                                    "app_name": self.model._meta.app_label,
                                                                    "table_name": self.model._meta.model_name,
                                                                    "selected_ids": selected_ids,
                                                                    "action": request._admin_action,
                                                                    "errors":errors
                                                                    })
    def default_form_validation(self):
        '''用户可以在此自义当前表的表单验证，相当于 djano form 的clean 方法'''
        pass

class CustomerAdmin(BaseAdmin):
    list_display = ['id','name','qq','source','consultant','consult_course','date','status',"enroll"]
    list_filters = ['source','consultant','consult_course','status',"qq","date"]
    search_fields = ['qq',"name","consultant__name"]    # consultant 是外键 要按名字搜索 要 __name
    filter_horizontal = ['tags',]
    #model = models.Customer
    ordering = "-date"
    readonly_fields = ["qq", "consultant","tags"]
    # readonly_table = True

    #自宝义字段，数据库里没有的
    def enroll(self):
         return  '''<a href="/crm/customers/%s/enrollment/">报名</a>'''%(self.instance.id)
    enroll.display_name = "报名链接"


    def default_form_validation(self):
        print("执行了 这个表的默认验证，content 不能小于6")

        if len(self.cleaned_data.get("content")) < 6 :
            return ValidationError(
                _('Field %(filed)s length is not lt 6 '),
                code="invalid",
                params={"filed": "content"},
             )



    #
    def clean_referral_from(self):
        print("name clean validation:", self.cleaned_data["referral_from"])
        print(self.cleaned_data)
        if not self.cleaned_data["referral_from"]:
            self.add_error('referral_from', "cannot be null")
        else:
            return self.cleaned_data["referral_from"]   #检查完一下要 return 该字段,不然 这字段就会是空的

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ("id",'customer','consultant','date')

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] =  admin_class

class UserProfileAdmin(BaseAdmin):
    list_display = ("email","name")
    readonly_fields = ("password",)
    filter_horizontal = ("user_permissions","groups")
    form_exclude_field = ("last_login",)

class EnrollmentAdmin(BaseAdmin):
    list_display = ("customer","enrollment_class",)

class CourseRcordAdmin(BaseAdmin):
    list_display = ['id','from_class','day_num','teacher','has_homework','homework_title',]

    def initialize_studyrecords(self,request,queryset):
        print('-------------->initialize_studyrecords',self,request,queryset)
        if len(queryset) >1 :
            return HttpResponse('只能选择一个班级')

        print(queryset[0].from_class.enrollment_set.all())
        try:
            for enroll_obj in queryset[0].from_class.enrollment_set.all():
                # models.StudyRecord.objects.get_or_create(
                #     student= enroll_obj,
                #     course_record= queryset[0],
                #     attendance= 0,
                #     score= 0,
                # )
                new_obj_list = []
                new_obj_list.append(models.StudyRecord(
                        student= enroll_obj,
                        course_record= queryset[0],
                        attendance= 0,
                        score= 0,
                ))
            models.StudyRecord.objects.bulk_create(new_obj_list)  #批量创建
        except Exception as e:
            return HttpResponse("已有本节课记录，不能再创建，请检查学习记录表！！")

        return  redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].id)
    initialize_studyrecords.display_name = "初始化本节所有员的上课记录"

    actions = ["initialize_studyrecords",]

class StudyRecordAdmin(BaseAdmin):
    list_display = ['student','course_record','attendance','score','date',]
    list_filters = ['course_record','score']
    list_editable = ['attendance',"score"]

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserProfileAdmin)
register(models.Enrollment,EnrollmentAdmin)
register(models.StudyRecord,StudyRecordAdmin)
register(models.CourseRecord,CourseRcordAdmin)