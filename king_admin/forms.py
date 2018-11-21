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

    attrs = {"Meta":Meta}
    model_class = type("DynamicModelClass",(ModelForm,),attrs)
    return  model_class







