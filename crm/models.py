from django.db import models
from django.contrib.auth.models import User


import pymysql



# # Create your models here.
#
class Customer(models.Model):
    #"客户信息表"
    name =models.CharField(max_length=32,null=True,blank=True)
    qq = models.CharField(max_length=64,unique=True)
    qq_name = models.CharField(max_length=64,blank=True,null=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    source_choices = ( (0,'转介绍'),
                       (1,'QQ群'),
                       (2,'官网'),
                       (3,'百度推广'),
                       (4,'51CTO'),
                       (5,'知乎'),
                       (6,'市场推广')
                      )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(verbose_name="转介绍人QQ",max_length=64,blank=True,null=True)
    consult_course = models.ForeignKey("Course",verbose_name="咨询课程",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag",blank=True,null=True)
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)   #顾问

    status_choices = ((0, '已报名'),
                      (1, '未报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=1)
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户表"            #在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "客户表"     #加上这和把s 去掉




class Tag(models.Model):
    name = models.CharField(max_length=32,unique=True)

    class Meta:
        verbose_name = "标签"  # 只加这个会显示客户表s ,
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class CustomerFollowUp(models.Model):
    #"客户跟 进表"
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟进内容")
    consultant =  models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date =  models.DateTimeField(auto_now_add=True)
    intention_chices = (
        (0,"2周内报名"),
        (1,"1周内报名"),
        (2,"近期无报名计划"),
        (3,"已在其它机构报名"),
        (4,"已拉黑"),
        (5,"已报名"),
    )
    intention = models.SmallIntegerField(choices=intention_chices)
    date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s,%s>"%(self.customer.qq,self.intention)

    class Meta:
        verbose_name = "客户跟进记录"            #在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "客户跟进记录"     #加上这和把s 去掉


class Course(models.Model):
    #"课程表"
    name =  models.CharField(max_length=64,unique=True)
    price =  models.PositiveSmallIntegerField()
    period = models.PositiveIntegerField(verbose_name="周期（月）")
    outline   =models.TextField()  #大纲

    class Meta:
        verbose_name = "课程表"            #在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "课程表"     #加上这和把s 去掉
    def __str__(self):
        return self.name


class Branch(models.Model):
    #"校区"
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "校区"            #在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "校区"     #加上这和把s 去掉

class ClassList(models.Model):
    "班级表"
    course =  models.ForeignKey("Course",on_delete=models.CASCADE)
    class_type_choices = ((0,"面授(脱产)"),
                          (1,"面授(周末)"),
                          (2,"网络班"),
    )
    class_type =  models.SmallIntegerField(choices=class_type_choices,verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    branch  = models.ForeignKey("Branch",on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="开班日期")
    end_date =  models.DateField(verbose_name="结业日期",blank=True,null=True)

    def  __str__(self):
        return "%s %s %s"%(self.branch,self.course,self.semester)

    class Meta:
        unique_together = ("branch","course","semester")
        verbose_name = "班级表"  # 在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "班级表"  # 加上这和把s 去掉


class CourseRecord(models.Model):
    "课程记录"
    from_class = models.ForeignKey("ClassList",verbose_name="班级",on_delete=models.CASCADE)
    day_num =  models.PositiveSmallIntegerField(verbose_name="第几天(节)")
    teacher = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    has_homework =  models.BooleanField(default=True)
    homework_title =  models.CharField(max_length=128,blank=True,null=True)
    outline =  models.TextField(verbose_name="本节课程大纲")
    date =  models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.from_class,self.day_num)

    class Meta:
        unique_together = ("from_class","day_num")
        verbose_name = "上课记录"  # 在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "上课记录"  # 加上这和把s 去掉



    pass

class StudyRecord(models.Model):
    "学习记录"
    student = models.ForeignKey("Enrollment",on_delete=models.CASCADE)
    course_record =  models.ForeignKey("CourseRecord",on_delete=models.CASCADE)
    attendance_choices = (
        (0,"已签到"),
        (1,"迟到"),
        (2,"缺席"),
        (3,"早退"),
   )
    attendance = models.SmallIntegerField(choices=attendance_choices,default=0)

    score_choices = (
        (100,"A+"),
        (90,"A"),
        (85,"B+"),
        (80,"B"),
        (75,"B-"),
        (70,"C+"),
        (60,"C"),
        (40,"C-"),
        (-50,"D"),
        (-100,"COPY"),
        (0,"N/A"),
    )
    score = models.SmallIntegerField(choices=score_choices,default=0)
    memo = models.TextField(blank=True,null=True)
    date  = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s"%(self.student,self.course_record,self.score)

    class Meta:
        unique_together = ("student","course_record")
        verbose_name = "学习记录"  # 在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "学习记录"  # 加上这和把s 去掉



class Enrollment(models.Model):
    "报表名"
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    enrollment_class =  models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)
    consultant =  models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False,verbose_name="学员已同意合同")
    contract_approved =  models.BooleanField(default=False,verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.customer,self.enrollment_class)

    class Meta:
        unique_together = ("customer","enrollment_class")
        verbose_name = "报名表"  # 在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "报名表"  # 加上这和把s 去掉




class Payment(models.Model):

    customer = models.ForeignKey("Enrollment",on_delete=models.CASCADE)
    course =  models.ForeignKey("Course",verbose_name="所报课程",on_delete=models.CASCADE)
    amount =  models.PositiveSmallIntegerField(verbose_name="数额",default=500)
    consultant =  models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "缴费表"  # 在django中表名显示中文，只加这个会显示客户表s ,
        verbose_name_plural = "缴费表"  # 加上这和把s 去掉

    def __str__(self):
        return "<%s %s>"%(self.customer,self.amount)


class UserProfile(models.Model):
    #"帐号表"
    #from django.contrib.auth.models import User
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role",blank=True,null=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    #"角色表"
   # id =  models.IntegerField(auto_created=True,primary_key=True)
   name = models.CharField(max_length=32,unique=True)
   menus = models.ManyToManyField("Menu",blank=True)

   def __str__(self):
       return self.name

   class Meta:
        verbose_name_plural = "角色表"  # 加上这和把s 去掉



class Menu(models.Model):
    name  = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)
    def __str__(self):
        return self.name








