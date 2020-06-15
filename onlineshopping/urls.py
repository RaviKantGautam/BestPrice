"""onlineshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from controller import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openadminlogin', openadminlogin),
    path('admin', openadminlogin),
    path('checkadminlogin', checkadminlogin),
    path('admindashboard', admindashboard),
    path('openadminchangepass', openadminchangepass),
    path('changeadminpassword', changeadminpassword),
    path('openstorechangepass', openstorechangepass),
    path('changestorepassword', changestorepassword),
    path('openmemberchangepass', openmemberchangepass),
    path('changememberpassword', changememberpassword),
    path('adminlogout', adminlogout),
    path('addcategorypage', addcategorypage),
    path('addcategoryaction', addcategoryaction),
    path('viewcategorypage', viewcategorypage),
    path('viewcategoryaction', viewcategoryaction),
    path('deletecategoryaction', deletecategoryaction),
    path('openaddproducts', openaddproducts),
    path('addproduct', addproduct),
    path('viewproducts', viewproducts),
    path('viewproductsmember', viewproductsmember),
    path('openviewproducts', openviewproducts),
    path('deleteproduct', deleteproduct),
    path('gotoeditproductpage', gotoeditproductpage),
    path('editproduct', editproduct),
    path('manageproductphotos', manageproductphotos),
    path('insertphoto', insertphoto),
    path('deleteproductphoto', deleteproductphoto),
    path('addstorepage', addstorepage),
    path('addstoreaction', addstoreaction),
    path('viewstorepage', viewstorepage),
    path('viewstoreaction', viewstoreaction),
    path('deletestoreaction', deletestoreaction),
    path('openeditstore', openeditstore),
    path('updatestoreaction', updatestoreaction),
    path('storelogin', storelogin),
    path('storeloginaction', storeloginaction),
    path('storehomepage', storehomepage),
    path('addstockpage', addstockpage),
    path('addstockaction', addstockaction),
    path('viewstockstore', viewstockstore),
    path('viewstockadmin', viewstockadmin),
    path('viewstorestockaction', viewstorestockaction),
    path('viewadminstockaction', viewadminstockaction),
    path('membersignuppage', membersignuppage),
    path('membersignupaction', membersignupaction),
    path('memberlogin', memberlogin),
    path('memberloginaction', memberloginaction),
    path('memberhomepage', memberhomepage),
    path('viewadminmembers', viewadminmembers),
    path('viewadminmembersaction', viewadminmembersaction),
    path('memberstatuschange', memberstatuschange),
    path('openuserdashboard', openuserdashboard),
    path('insertcart', insertcart),
    path('viewfilteredproducts', viewfilteredproducts),
    path('addtocart', addtocart),
    path('viewcart', viewcart),
    path('productdetailpage', productdetailpage),
    path('', website),
    path('about', about),
    path('contact', contact),
    path('vieworders', vieworders),
    path('deleteitemfromcart', deleteitemfromcart),
    path('fetchorders', fetchorders),
    path('orderdetail', orderdetail),
    path('getallproducts', getallproducts),
    path('gotoproductdetailfromhome', gotoproductdetailfromhome),
    path('openstoresellstock', openstoresellstock),
    path('openstoreviewreport', openstoreviewreport),
    path('verifymember', verifymember),
    path('verifyproduct', verifyproduct),
    path('sellstock', sellstock),
    path('fetchordersstore', fetchordersstore),
    path('orderdetailstore', orderdetailstore),
    path('memberlogout', memberlogout),
    path('storelogout', storelogout),
    path('sendotponphone', sendotponphone),
    path('sendpassadmin', sendpassadmin),
    path('sendpassstore', sendpassstore),
    path('sendpassmember', sendpassmember)
]
