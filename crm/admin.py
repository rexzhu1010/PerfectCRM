from django.contrib import admin
from django.shortcuts import render

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import render,redirect,HttpResponse


from crm import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','qq','name','source','consultant','content','status','date')
    list_filter = ('source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)
    list_per_page = 5
    #readonly_fields = ('qq','consultant')
    #ordering =


    # actions = ["test_action", ]
    #
    #
    # def test_action(self,request,arg2):
    #     print('test action:',self,request,arg2)
    #     return render(request,"king_admin/table_index.html")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')


class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',"template")

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin','is_active','is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('name','stu_account')}),
        ('Permissions', {'fields': ('is_admin','is_active',"groups","user_permissions","roles")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("groups","user_permissions")

# Now register the new UserAdmin...

class CourseRcordAdmin(admin.ModelAdmin):
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

        return  redirect("/admin/crm/studyrecord/?course_record__id__exact=%s"%queryset[0].id)
    initialize_studyrecords.short_description = "初始化本节所有员的上课记录"

    actions = [initialize_studyrecords,]


class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ['id','student','course_record','attendance','score','date',]
    list_filter = ['course_record','score','attendance','course_record__from_class','student']
    list_editable = ['attendance',"score"]

class EnollmentAdmin(admin.ModelAdmin):
    list_display = ['id','customer',]


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment,EnollmentAdmin)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord,CourseRcordAdmin)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord,StudyRecordAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Menu)
admin.site.register(models.ContractTemplate,ContractTemplateAdmin)




