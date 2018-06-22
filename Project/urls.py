"""Project URL Configuration

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
from django.conf.urls import url

from website import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url('query/', views.query),
    url('result/', views.result),
    url(r'staff_login/', views.staff_login),
    url(r'staff_login_resu/', views.staff_login_resu),
    url(r'user_login/', views.user_login),
    url(r'user_login_resu/', views.user_login_resu),
    url(r'user_query/', views.user_query),
    url(r'user_resu/', views.user_resu),
    url(r'staff_input/',views.staff_input),
    url(r'saomiao/',views.saomiao),
    url(r'paisong/',views.paisong),
    url(r'address_add/',views.address_add),
    url(r'address_change/',views.address_change),
    url(r'address_delete/',views.address_delete),
    url(r'user_register',views.user_register),
    url(r'staff_register',views.staff_register),
    url(r'user_registe_resu',views.user_registe_resu),
    url(r'staff_registe_resu',views.staff_registe_resu)

]
