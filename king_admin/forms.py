# rex.zhu
from  django.forms import forms,ModelForm

from crm import  models

class  CustomerModelForm(ModelForm):

    class Meta:
       model = models.Customer
       fields = "__all__"



def  create_model_form(request,admin_class):
    class Meta:
        model =  admin_class.model
        fields = "__all__"


    def __new__(cls,*args,**kwargs):

            for field_name,field_obj in  cls.base_fields.items():
                 field_obj.widget.attrs['class'] = 'form-control'
                 # print(field_name,dir(field_obj))
                 # field_obj.widget.attrs['maxlength'] = getattr(field_obj,"max_length") if hasattr(field_obj,"max_length") else ""
            return ModelForm.__new__(cls)

    attrs = {"Meta":Meta}
    model_class = type("DynamicModelClass",(ModelForm,),attrs)
    setattr(model_class,"__new__",__new__)
    return  model_class







