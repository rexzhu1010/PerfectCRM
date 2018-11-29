# rex.zhu
from  django.forms import forms,ModelForm

from crm import  models

class  CustomerModelForm(ModelForm):

    class Meta:
       model = models.Customer
       fields = "__all__"



def  create_model_form(request,admin_class):
    #创建model form 方法 中需要的 meta
    class Meta:
        model =  admin_class.model
        fields = "__all__"


    #这里自定义 __new__方法，用来生成类时使用
    #__new__是在新式类中新出现的方法，它作用在构造方法建造实例之前，在这里可以自定义修改类中内容，比如给modelform 增加 css，修改CSS
    def __new__(cls,*args,**kwargs):

            for field_name,field_obj in  cls.base_fields.items():
                 field_obj.widget.attrs['class'] = 'form-control'
                 # print(field_name,field_obj)
                 # field_obj.widget.attrs['maxlength'] = getattr(field_obj,"max_length") if hasattr(field_obj,"max_length") else ""
                 print(admin_class.readonly_fields)
                 if field_name in  admin_class.readonly_fields:
                     field_obj.widget.attrs['disabled']="disabled"

            return ModelForm.__new__(cls)

    attrs = {"Meta":Meta}
    #创建动态类
    model_class = type("DynamicModelClass",(ModelForm,),attrs)
    setattr(model_class,"__new__",__new__)
    return  model_class







