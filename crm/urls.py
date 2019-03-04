# rex.zhu


from django.conf.urls import url
from crm import  views
urlpatterns = [
    url(r"^$",views.index,name="sales_index"),
    url(r"^customers/$",views.customer_list,name="customers_list"),
    url(r'customers/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    url(r'customers/stu_registration/(\d+)/(\w+)/$', views.student_registration, name="student_registration"),
    url(r'contract_review/(\d+)/$', views.contract_review, name="contract_review"),
    url(r'payment/(\d+)/$', views.payment, name="payment"),
    url(r'enrollment_rejection/(\d+)/$',views.enrollment_rejection,name="enrollment_rejection")
]
