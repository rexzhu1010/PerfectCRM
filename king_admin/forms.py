# rex.zhu
from  django.forms import forms,ModelForm
from king_admin import utils
from django.forms import  ValidationError
from  django.utils.translation import  ugettext as _

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
        # exclude = ("qq",)
        exclude = admin_class.form_exclude_field

    #这里自定义 __new__方法，用来生成类时使用
    #__new__是在新式类中新出现的方法，它作用在构造方法建造实例之前，在这里可以自定义修改类中内容，比如给modelform 增加 css，修改CSS
    def __new__(cls,*args,**kwargs):

            for field_name,field_obj in  cls.base_fields.items():
                 field_obj.widget.attrs['class'] = 'form-control'
                 # print(field_name,field_obj)
                 # field_obj.widget.attrs['maxlength'] = getattr(field_obj,"max_length") if hasattr(field_obj,"max_length") else ""

                 if not admin_class.is_add_form:
                     if field_name in  admin_class.readonly_fields:
                         field_obj.widget.attrs['disabled']="disabled"

                 if hasattr(admin_class, "clean_%s" % field_name):
                     field_clean_func = getattr(admin_class, "clean_%s" % field_name)
                     setattr(cls, "clean_%s" % field_name, field_clean_func)




            return ModelForm.__new__(cls)

    def  defaut_clean(self):
        #这个默认验证是给所有的form 加一个 form  只读认证"
        print("保存前 cleaned_data:", self.cleaned_data)
        print("-----------running default clean")
        error_list=[]
        #如果是修改，做以下验证，验证只读字段，不能修改

        if admin_class.readonly_table :
            print("这个是只读table")
            raise  ValidationError(
                _('Table is readonly '),
                code="invalid",
                params={}, )

        if self.instance.id:
            print("这个form 表单有 instance")
            for filed in admin_class.readonly_fields:
                filed_val =  getattr(self.instance,filed)
                filed_frontend_val =self.cleaned_data.get(filed)
                # print(filed_val,filed_frontend_val)

                #如果是多对多
                if hasattr(filed_val,"select_related"):
                    print(set(filed_val.all()),set(filed_frontend_val))
                    if set(filed_val.all()) != set(filed_frontend_val) :
                        print("we are not same!!!!!!!")
                        if filed_frontend_val != filed_val:
                            self.add_error(filed,"%s cat not change"%filed)
                    continue

                #普通字段
                if filed_frontend_val != filed_val:
                    error_list.append( ValidationError(
                            _('Field %(filed)s is readonly ,data should be %(val)s'),
                            code="invalid",
                            params={"filed":filed,"val":filed_val},)
                    )




            response = admin_class.default_form_validation(self)
            if response:
                    error_list.append(response)
            if error_list:
                raise ValidationError(error_list)

        print("--------end default clean")
    #     # print(self.instance,request.POST)
    #
    #     #invoke user's cutomized form validation


    attrs = {"Meta":Meta}
    #创建动态类


    model_class = type("DynamicModelClass",(ModelForm,),attrs)
    setattr(model_class,"__new__",__new__)
    setattr(model_class,"clean",defaut_clean)

    return  model_class







