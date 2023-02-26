"""djangoFinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),

    path('SignUp', views.SignUp, name='SignUp'),
    path('EmpSignUp', views.EmpSignUp, name='EmpSignUp'),
    path('SignIn', views.SignIn, name='SignIn'),
    path('SignOut', views.SignOut, name='SignOut'),

    path('Shop', views.Shop, name='Shop'),

    path('Dashboard', views.Dashboard, name='Dashboard'),

    path('CustomerList', views.CustomerList, name='CustomerList'),
    path('CustomerNew', views.CustomerNew, name='CustomerNew'),
    path('CustomerEdit/<cid>', views.CustomerEdit, name='CustomerEdit'),
    path('CustomerDelete/<cid>', views.CustomerDelete, name='CustomerDelete'),

    path('ProductTypeList', views.ProductTypeList, name='ProductTypeList'),
    path('ProductTypeNew', views.ProductTypeNew, name='ProductTypeNew'),
    path('ProductTypeEdit/<id>', views.ProductTypeEdit, name='ProductTypeEdit'),
    path('ProductTypeDelete/<id>', views.ProductTypeDelete, name='ProductTypeDelete'),

    path('EmployeeList', views.EmployeeList, name='EmployeeList'),
    path('EmployeeNew', views.EmployeeNew, name='EmployeeNew'),
    path('EmployeeEdit/<eid>', views.EmployeeEdit, name='EmployeeEdit'),
    path('EmployeeDelete/<eid>', views.EmployeeDelete, name='EmployeeDelete'),

    path('ProductList', views.ProductList, name='ProductList'),
    path('ProductNew', views.ProductNew, name='ProductNew'),
    path('ProductEdit/<pid>', views.ProductEdit, name='ProductEdit'),
    path('ProductDelete/<pid>', views.ProductDelete, name='ProductDelete'),

    path('Basket', views.Basket, name='Basket'),
    path('ClearBasket', views.ClearBasket, name='ClearBasket'),
    path('CartSutmit', views.CartSutmit, name='CartSutmit'),
    path('SubmitOrder', views.SubmitOrder, name='SubmitOrder'),
    path('ViewOrder', views.ViewOrder, name='ViewOrder'),
    path('DetailOrder/<oid>', views.DetailOrder, name='DetailOrder'),
    path('OrderConfirm/<oid>', views.OrderConfirm, name='OrderConfirm'),
    path('OrderReject/<oid>', views.OrderReject, name='OrderReject'),
    path('MoneyTransfer/<oid>', views.MoneyTransfer, name='MoneyTransfer'),
    path('MoneyAccept/<oid>', views.MoneyAccept, name='MoneyAccept'),
    path('ProductSend/<oid>', views.ProductSend, name='ProductSend'),
    path('OrderCancel/<oid>', views.OrderCancel, name='OrderCancel'),
]
