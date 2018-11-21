from django.contrib import admin
from crm import  models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id',"name",'qq','source','consultant','content','status','date')
    list_filter = ('source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)

class CustomerFollowUpAdmin(admin.ModelAdmin):
    list_display = ('id',"customer",'consultant','content','date')




admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.CourseRecord)
admin.site.register(models.CustomerFollowUp,CustomerFollowUpAdmin)
admin.site.register(models.Enrollment)
admin.site.register(models.Payment)
admin.site.register(models.Role)
admin.site.register(models.StudyRecord)
admin.site.register(models.Tag)
admin.site.register(models.UserProfile)
admin.site.register(models.Menu)


# Register your models here.
