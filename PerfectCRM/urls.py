"""PerfectCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from PerfectCRM import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r"^$",include("crm.urls") ),
    url(r'^admin/', admin.site.urls),
    url(r'^crm/',include("crm.urls")),
    url(r'^accounts/login/$',views.acc_login),
    url(r'^accounts/logout/$',views.acc_logout,name="acc_logout"),
    url(r'^student/',include("student.urls")),
    url(r'^king_admin/', include("king_admin.urls")),

]
