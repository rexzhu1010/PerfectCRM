# rex.zhu


from django.forms import ModelForm
from crm import  models


class EnrollmentForm(ModelForm):
    def __new__(cls,*args,**kwargs):
            for field_name,field_obj in  cls.base_fields.items():
                 field_obj.widget.attrs['class'] = 'form-control'

            return ModelForm.__new__(cls)

    class Meta:
            model = models.Enrollment
            fields = ['enrollment_class','consultant']



class CustomerForm(ModelForm):
    def __new__(cls,*args,**kwargs):
            for field_name,field_obj in  cls.base_fields.items():
                field_obj.widget.attrs['class'] = 'form-control'
                if  field_name in cls.Meta.readonly:
                    field_obj.widget.attrs['disabled'] =  "disabled"
            return ModelForm.__new__(cls)

    class Meta:
        model  = models.Customer
        fields = "__all__"
        exclude = ["content","memo","tags","referral_from","consult_course"]
        readonly = ["qq","source","consultant"]

    def clean(self):
        print("我是默认验证")
        for  filed in self.Meta.readonly:
            filed_val = getattr(self.instance, filed)
            filed_frontend_val = self.cleaned_data.get(filed)
            if filed_frontend_val != filed_val:
                self.add_error("__all__", "小样的，别乱改！！！")




class PaymentForm(ModelForm):
    def __new__(cls,*args,**kwargs):
            for field_name,field_obj in  cls.base_fields.items():
                field_obj.widget.attrs['class'] = 'form-control'
                if  field_name in cls.Meta.readonly:
                    field_obj.widget.attrs['disabled'] =  "disabled"
            return ModelForm.__new__(cls)
    class Meta:
            model =  models.Payment
            fields = "__all__"
            readonly = []