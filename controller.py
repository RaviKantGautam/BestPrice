from datetime import date
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from myconnection import *
import http.client
import time

def website(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def vieworders(request):
    if request.session.has_key('MEMBERID'):
        request.session['page'] = 'vieworders'
        return render(request, 'vieworders.html')
    else:
        return HttpResponseRedirect('memberlogin')



def openadminlogin(request):
    return render(request,'adminlogin.html')

@csrf_exempt
def checkadminlogin(request):
    email=request.POST['email']
    password=request.POST['password']
    conn=myconnection.connect('')
    cr=conn.cursor()
    query="select * from admin where email='"+email+"' and password='"+password+"'"
    cr.execute(query)
    result=cr.fetchone()
    if result==None:
        return render(request,'adminlogin.html',{"message":'invalid email/password'})
    else:
        request.session['adminemail']=email
        request.session['adminname'] = result[4]
        request.session['admintype'] = result[2]
        return render(request,'admindashboard.html')
def admindashboard(request):
    if request.session.has_key('adminemail'):
        return render(request, 'admindashboard.html')
    else:
        return render(request, 'adminlogin.html')
def openadminchangepass(request):
    return render(request,'adminchangepassword.html')
def changeadminpassword(request):
    oldpass = request.POST['oldpass']
    newpass = request.POST['newpass']
    conn = myconnection.connect('')
    cr = conn.cursor()
    email=""
    if request.session.has_key('adminemail'):
        email = request.session['adminemail']
        query = "select * from admin where email='" + email + "' and password='" + oldpass + "'"
        cr.execute(query)
        result = cr.fetchone()
        if result == None:
            return render(request, 'adminchangepassword.html', {"message": 'old password not match!!'})
        else:
            query = "update admin set password='" + newpass + "' where email='" + email + "'"
            cr.execute(query)
            conn.commit()
            return render(request, 'adminchangepassword.html', {"message": 'password changed successfully!!'})
    else:
        return HttpResponseRedirect('openadminlogin')
def adminlogout(request):
    if request.session.has_key('adminemail'):
        del request.session['adminemail']
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def storelogout(request):
    if request.session.has_key('STOREEMAIL'):
        del request.session['STOREEMAIL']
        del request.session['STOREID']
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def memberlogout(request):
    if request.session.has_key('MEMBEREMAIL'):
        del request.session['MEMBEREMAIL']
        del request.session['MEMBERID']
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


# new functions
def addcategorypage(request):
    return render(request, 'addcategorypage.html')


def addcategoryaction(request):
    conn = myconnection.connect('')
    cname = request.GET['cname']
    description = request.GET['description']
    cr = conn.cursor()
    s = "insert into category values ('" + cname + "','" + description + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Data not saved"
    return JsonResponse(d, safe=False)

def viewcategorypage(request):
    return render(request, 'viewcategorypage.html')


def viewcategoryaction(request):
    conn = myconnection.connect('')
    s = "select * from category"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['cname'] = p[0]
        d['description'] = p[1]
        x.append(d)
    return JsonResponse(x, safe=False)
def deletecategoryaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    cname = request.GET['cname']
    s = "delete from category where cname='" + cname + "'"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    return HttpResponseRedirect('/viewcategorypage')

def addstorepage(request):
    return render(request, 'addstore.html')


def addstoreaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    title = request.GET['title']
    email = request.GET['email']
    password = request.GET['password']
    location = request.GET['location']
    mobile = request.GET['mobile']
    s = "insert into stores values (NULL,'" + title + "','" + email + "','" + password + "','" + location + "','" + mobile + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Data not saved"
    return JsonResponse(d, safe=False)


def viewstorepage(request):
    return render(request, 'viewstore.html')


def viewstoreaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    s = "select * from stores"
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['storeid'] = p[0]
        d['title'] = p[1]
        d['email'] = p[2]
        d['password'] = p[3]
        d['location'] = p[4]
        d['mobile'] = p[5]
        x.append(d)
    return JsonResponse(x, safe=False)
def deletestoreaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    storeid = request.GET['storeid']
    s = "delete from stores where storeid='" + storeid + "'"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    return HttpResponseRedirect('/viewstorepage')

def openeditstore(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    storeid=request.GET['storeid']
    s = "select * from stores where storeid='"+storeid+"'"
    cr.execute(s)
    p = cr.fetchone()
    d = {}
    d['storeid'] = p[0]
    d['title'] = p[1]
    d['email'] = p[2]
    d['password'] = p[3]
    d['location'] = p[4]
    d['mobile'] = p[5]
    return render(request, 'editstore.html', {'mydata': d})

def updatestoreaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    storeid=request.GET['storeid']
    title = request.GET['title']
    email = request.GET['email']
    password = request.GET['password']
    location = request.GET['location']
    mobile = request.GET['mobile']
    s = "update  stores set title='" + title + "',emailid='" + email + "',password='" + password + "',location='" + location + "',mobilenumber='" + mobile + "' where storeid='"+storeid+"'"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Data not saved"
    return JsonResponse(d, safe=False)


def storelogin(request):
    return render(request,'storelogin.html')
@csrf_exempt
def storeloginaction(request):
    email = request.POST['email']
    password = request.POST['password']
    conn = myconnection.connect('')
    cr = conn.cursor()
    flag = False
    s = "select * from stores"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        if p[2]==email and p[3]==password:
            request.session['STOREEMAIL'] = email
            request.session['STORETITLE'] =p[1]
            request.session['STOREID']=p[0]
            flag = True
            break

    d = {}
    if flag==False:
        d['message'] = "Invalid Login"
    else:
        d['message'] = "Login Success"

    return JsonResponse(d,safe=False)
def storehomepage(request):
    if request.session.has_key('STOREID'):
        return render(request, 'storehomepage.html')
    else:
        return HttpResponseRedirect('storelogin')

def addstockpage(request):
    if request.session.has_key('STOREID'):
        return render(request, 'addstock.html')
    else:
        return HttpResponseRedirect('storelogin')

def addstockaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    productid = request.GET['productid']
    qt="select * from products where productid='"+str(productid)+"'"
    cr.execute(qt)
    rs=cr.fetchone()
    d = {}
    if rs==None:
        d['message'] = "Invalid Product ID"
    else:
        quantity = request.GET['quantity']
        storeid = request.GET['storeid']
        dateofpurchase = request.GET['dateofpurchase']
        dateofexpiry = request.GET['dateofexpiry']
        s = "insert into stock values (NULL,'" + productid + "','" + quantity + "','" + storeid + "','" + dateofexpiry + "','" + dateofpurchase + "')"
        result = cr.execute(s)
        conn.commit()
        conn.close()

        if result == 1:
            d['message'] = "Data saved"
        else:
            d['message'] = "Data not saved"



    return JsonResponse(d, safe=False)
def viewstockstore(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    x = []
    s = "select * from category"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['categoryname'] = p[0]
        x.append(d)
    return render(request, 'viewstockstore.html', {'mydata': x})
def viewstockadmin(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    x = []
    s = "select * from category"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['categoryname'] = p[0]
        x.append(d)
    y = []
    s = "select * from stores"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['storeid'] = p[0]
        d['title'] = p[1]
        y.append(d)
    z=[]
    z.append(x)
    z.append(y)
    return render(request, 'viewstockadmin.html', {'mydata': z})
def viewstorestockaction(request):
    if request.session.has_key('STOREID'):
        conn = myconnection.connect('')
        cr = conn.cursor()
        cname = request.GET['cname']
        s = "select productid from products where cname='" + cname + "'"
        cr.execute(s)
        result = cr.fetchall()
        pids = []
        for p in result:
            pids.append(p[0])
        print(pids)
        storeid=request.session['STOREID']
        s = "select * from stock where storeid='"+str(storeid)+"'"
        cr.execute(s)
        result = cr.fetchall()
        x = []
        for p in result:
            if p[1] in pids:
                print(p[1])
                d = {}
                d['stockid'] = p[0]
                d['productid'] = p[1]
                s = "select productname from products where productid='" + str(p[1]) + "'"
                cr.execute(s)
                rs = cr.fetchone()
                d['productname'] = rs[0]
                d['quantity'] = p[2]
                d['storeid'] = p[3]
                d['dateofexpiry'] = p[4]
                d['dateofpurchase'] = p[5]
                x.append(d)
        conn.close()
        return JsonResponse(x, safe=False)
    else:
        return HttpResponseRedirect('storelogin')


def viewadminstockaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    cname=request.GET['cname']
    storeid=request.GET['storeid']
    s="select productid from products where cname='"+cname+"'"
    cr.execute(s)
    result=cr.fetchall()
    pids=[]
    for p in result:
        pids.append(p[0])
    print(pids)
    s = "select * from stock where storeid='"+str(storeid)+"'"
    cr.execute(s)
    result = cr.fetchall()
    x = []
    for p in result:
        if p[1] in pids:
            print(p[1])
            d = {}
            d['stockid'] = p[0]
            d['productid'] = p[1]
            s = "select productname from products where productid='" +str(p[1]) + "'"
            cr.execute(s)
            rs = cr.fetchone()
            d['productname']=rs[0]
            d['quantity'] = p[2]
            d['storeid'] = p[3]
            d['dateofexpiry'] = p[4]
            d['dateofpurchase'] = p[5]
            x.append(d)
    conn.close()
    return JsonResponse(x, safe=False)

def membersignuppage(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    y = []
    s = "select * from stores"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['storeid'] = p[0]
        d['title'] = p[1]
        y.append(d)
    return render(request, 'membersignup.html', {'mydata': y})

@csrf_exempt
def membersignupaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    parentstore = request.POST['parentstore']
    email = request.POST['email']
    password = request.POST['password']
    mobile = request.POST['mobile']
    name = request.POST['name']
    poc = request.POST['poc']
    cardname1 = request.POST['cardname1']
    cardname2 = request.POST['cardname2']
    cardname3 = request.POST['cardname3']
    s = "insert into members values (NULL,'" + name + "','" + poc + "','" + mobile + "','" + email + "','" + password + "','" + cardname1 + "','" + cardname2 + "','" + cardname3 + "','" + parentstore + "','pending')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Signup Fail"
    return JsonResponse(d, safe=False)

def memberlogin(request):
    return render(request,'memberlogin.html')

@csrf_exempt
def memberloginaction(request):
    email = request.POST['email']
    password = request.POST['password']
    conn = myconnection.connect('')
    cr = conn.cursor()
    flag = False
    s = "select * from members"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        if p[4]==email and p[5]==password and p[10]=='approved':
            request.session['MEMBEREMAIL'] = email
            request.session['MEMBERNAME'] = p[1]
            request.session['MEMBERID'] = p[0]
            flag = True
            break

    d = {}
    if flag==False:
        d['message'] = "Invalid Login"
    else:
        d['message'] = "Login Success"

    return JsonResponse(d,safe=False)
def memberhomepage(request):
    if request.session.has_key('MEMBERID'):
        conn = myconnection.connect('')
        cr = conn.cursor()
        x = []
        s = "select * from stores"
        cr.execute(s)
        result = cr.fetchall()
        for p in result:
            d = {}
            d['storeid'] = p[0]
            d['title'] = p[1]
            x.append(d)
        request.session['page'] = 'userdashboard'
        return render(request, 'memberhome.html', {'mydata': x})
    else:
        return HttpResponseRedirect('memberlogin')


def viewadminmembers(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    y = []
    s = "select * from stores"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['storeid'] = p[0]
        d['title'] = p[1]
        y.append(d)
    return render(request, 'approvemembers.html', {'mydata': y})
def viewadminmembersaction(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    storeid=request.GET['storeid']
    s="select * from members where parentstore='"+storeid+"' and status='pending'"
    cr.execute(s)
    result=cr.fetchall()
    x = []
    for p in result:
        d = {}
        d['memberid'] = p[0]
        d['name'] = p[1]
        d['poc'] = p[2]
        d['mobile'] = p[3]
        d['email'] = p[4]
        d['password'] = p[5]
        d['cardname1'] = p[6]
        d['cardname2'] = p[7]
        d['cardname3'] = p[8]
        d['parentstore'] = p[9]
        d['status']=p[10]
        x.append(d)
    s = "select * from members where parentstore='" + storeid + "' and status='approved'"
    cr.execute(s)
    result = cr.fetchall()
    y = []
    for p in result:
        d = {}
        d['memberid'] = p[0]
        d['name'] = p[1]
        d['poc'] = p[2]
        d['mobile'] = p[3]
        d['email'] = p[4]
        d['password'] = p[5]
        d['cardname1'] = p[6]
        d['cardname2'] = p[7]
        d['cardname3'] = p[8]
        d['parentstore'] = p[9]
        d['status'] = p[10]
        y.append(d)
    z=[]
    z.append(x)
    z.append(y)

    conn.close()
    return JsonResponse(z, safe=False)


def memberstatuschange(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    memberid = request.GET['memberid']
    opr=request.GET['opr']
    s=""
    if opr=='approve':
        s="update members set status='approved' where memberid='"+memberid+"'"
    else:
        s = "update members set status='pending' where memberid='" + memberid + "'"
    cr.execute(s)
    conn.commit()
    conn.close()
    return HttpResponseRedirect('/viewadminmembers')

# new functions
def openaddproducts(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    x = []
    s = "select * from category"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['categoryname'] = p[0]
        x.append(d)
    return render(request, 'addproducts.html', {'mydata': x})
@csrf_exempt
def addproduct(request):
    print()
    conn = myconnection.connect('')
    cr = conn.cursor()
    categoryname = request.POST['categoryname']
    pname = request.POST['pname']
    price = request.POST['price']
    mrp = request.POST['mrp']
    description = request.POST['description']
    photo = request.FILES['photo']
    brand = request.POST['brand']
    fs = FileSystemStorage()
    filename = fs.save(photo.name, photo)
    location = fs.url(filename)
    s = "insert into products values (null,'" + pname + "','" + price + "','" + mrp + "','" + description + "','" + brand + "','" + categoryname + "','" + filename + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    d['message'] = "Data saved"
    return render(request,'addproducts.html',d)
def openviewproducts(request):
    return render(request,'viewproducts.html')
def viewproducts(request):
    conn=myconnection.connect('')
    cr=conn.cursor()
    query="select * from products"
    cr.execute(query)
    result=cr.fetchall()
    list=[]
    for row in result:
        list.append(row)
    return JsonResponse(list,safe=False)
def viewproductsmember(request):
    conn=myconnection.connect('')
    cr=conn.cursor()
    storeid=request.GET['storeid']
    print(storeid)
    q1="select productid from stock where storeid='"+str(storeid)+"'"
    cr.execute(q1)
    pids=[]
    rso=cr.fetchall()
    for p in rso:
        pids.append(p[0])
    print(pids)
    query="select * from products"
    cr.execute(query)
    result=cr.fetchall()
    list=[]
    for row in result:
        if row[0] in pids:
            list.append(row)
    print(list)
    return JsonResponse(list,safe=False)
def viewfilteredproducts(request):
    conn=myconnection.connect('')
    cr=conn.cursor()
    value=request.GET['value']
    query="select * from products where productname LIKE '"+value+"%'"
    cr.execute(query)
    result=cr.fetchall()
    list=[]
    for row in result:
        list.append(row)
    return JsonResponse(list,safe=False)
def deleteproduct(request):
    pid=request.GET['pid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "delete  from products where productid='"+str(pid)+"'"
    cr.execute(query)
    conn.commit()
    return HttpResponse('success')
def gotoeditproductpage(request):
    conn = myconnection.connect('')
    cr = conn.cursor()
    productid = request.GET['pid']
    x = []
    s = "select * from category"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['categoryname'] = p[0]
        x.append(d)
    y = []
    s = "select * from products where productid='" + productid + "'"
    cr.execute(s)
    p = cr.fetchone()
    conn.close()
    d = {}
    d['productid'] = p[0]
    d['productname'] = p[1]
    d['description'] = p[4]
    d['price'] = p[2]
    d['priceafterdiscount'] = p[3]
    d['productphoto'] = p[7]
    d['cname'] = p[6]
    d['brand'] = p[5]
    y.append(d)
    z = []
    z.append(x)
    z.append(y)
    return render(request, 'editproduct.html', {'mydata': z})
@csrf_exempt
def editproduct(request):
    print()
    categoryname = request.POST['categoryname']
    pname = request.POST['pname']
    price = request.POST['price']
    mrp = request.POST['mrp']
    description = request.POST['description']
    brand = request.POST['brand']
    productid = request.POST['productid']
    hidden =request.POST['hidden']
    query=""
    fs = FileSystemStorage()
    if hidden=="nofile":
        query = "update products  set productname='" + pname + "',price='" + price + "',priceafterdiscount='" + mrp + "',description='" + description + "',brand='"+brand+"',cname='" + categoryname + "' where productid='"+productid+"'"
    else:
        photo = request.FILES['photo']
        fs.save( photo.name, photo)
        query ="update products  set productname='" + pname + "',price='" + price + "',priceafterdiscount='" + mrp + "',description='" + description + "',brand='"+brand+"',cname='" + categoryname + "',photo='" + photo.name + "' where productid='"+productid+"'"
    conn=myconnection.connect('')
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    return HttpResponse('success')
def manageproductphotos(request):
    pid=request.GET['pid']
    conn = myconnection.connect('')
    cr=conn.cursor()
    query="select * from photos where pid='"+str(pid)+"'"
    cr.execute(query)
    result=cr.fetchall()
    x=[]
    for row in result:
        d={}
        d['photoid']=row[0]
        d['pid'] = row[1]
        d['photopath'] = row[2]
        d['type'] = row[3]
        x.append(d)
    list=[]
    list.append(x)
    list.append(pid)
    return render(request,'manageproductphotos.html',{"data":list})
@csrf_exempt
def insertphoto(request):
    pid= request.POST['pid']
    type=request.POST['type']
    fs=FileSystemStorage()
    photo=request.FILES['photo']
    fs.save(photo.name,photo)
    conn=myconnection.connect('')
    cr=conn.cursor()
    query="insert into photos values(NULL,'"+str(pid)+"','"+str(photo.name)+"','"+str(type)+"')"
    cr.execute(query)
    conn.commit()
    return HttpResponseRedirect('manageproductphotos?pid='+pid)
def deleteproductphoto(request):
    photoid=request.GET['photoid']
    pid=request.GET['pid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "delete  from photos where photoid='" + str(photoid) + "'"
    cr.execute(query)
    conn.commit()
    return HttpResponseRedirect('manageproductphotos?pid=' + pid)
def openuserdashboard(request):
    request.session['page'] = 'userdashboard'
    return render(request,'userdashboard.html')
def addtocart(request):
    current_milli_time = int(round(time.time() * 1000))
    pid=request.GET['pid']
    quantity= request.GET['quantity']
    storeid=request.GET['storeid']
    print(quantity," ",pid)
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from products where productid='" + str(pid) + "'"
    cr.execute(query)
    row = cr.fetchone()
    d = {}
    d['pid'] = pid
    d['pname'] = row[1]
    d['price'] = row[2]
    d['priceafterdiscount'] = row[3]
    d['description'] = row[4]
    d['brand'] = row[5]
    d['cname'] = row[6]
    d['photo'] = row[7]
    netprice=(float)( row[3])
    totalprice=netprice*(int)(quantity)
    d['netprice']=netprice
    d['quantity']=quantity
    d['totalprice'] = totalprice
    d['ct']=current_milli_time
    d['storeid']=storeid
    if request.session.has_key('cart'):
        list=request.session['cart']
        list.append(d)
        request.session['cart']=list
        request.session['cartsize']=len(list)
    else:
        list = []
        list.append(d)
        request.session['cart'] = list
        request.session['cartsize'] = len(list)
    return HttpResponse('success')
def deleteitemfromcart(request):
    pid=request.GET['pid']
    ct = request.GET['ct']
    list = request.session['cart']
    newlist=[]
    for row in list:
        print(row['ct']," ",ct)
        if row['pid']==pid and str(row['ct'])==str(ct):
            print()
        else:
            newlist.append(row)
    request.session['cart'] = newlist
    request.session['cartsize'] = len(newlist)
    if len(newlist)==0:
        del request.session['cart']
        del request.session['cartsize']
    return HttpResponseRedirect('viewcart')
def viewcart(request):
    if request.session.has_key('MEMBERID'):
        if request.session.has_key('cart'):
            x = request.session['cart']
            totalcartbill = 0
            for item in x:
                totalcartbill = totalcartbill + (float)(item['totalprice'])
            list = []
            list.append(x)
            list.append(totalcartbill)
            list.append(totalcartbill * 100)
            request.session['page'] = 'viewcart'
            return render(request, 'viewcart.html', {"data": list})
        else:
            return HttpResponseRedirect('memberhomepage')

    else:
        return HttpResponseRedirect('memberlogin')

def productdetailpage(request):
    pid = request.GET['pid']
    storeid=request.GET['storeid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from photos where pid='" + str(pid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    for row in result:
        d = {}
        d['photoid'] = row[0]
        d['pid'] = row[1]
        d['photopath'] = row[2]
        d['type'] = row[3]
        x.append(d)
    list = []
    list.append(x)
    query = "select * from products where productid='" + str(pid) + "'"
    cr.execute(query)
    row = cr.fetchone()
    d = {}
    d['pid'] = pid
    d['pname'] = row[1]
    d['description'] = row[4]
    d['price'] = row[2]
    d['priceafterdiscount'] = row[3]
    d['brand']=row[5]
    d['photo'] = row[7]
    d['cname'] = row[6]
    d['storeid']=storeid
    list.append(d)
    return  render(request,'productdetail.html',{"data":list})
def insertcart(request):
    if request.session.has_key('cart'):
        memberid = request.POST['memberid']
        modeofbill = request.POST['modeofbill']
        totalbill = request.POST['totalbill']
        address=request.POST['address']
        conn = myconnection.connect('')
        cr = conn.cursor()
        td = date.today()
        sm="select * from members where memberid='"+str(memberid)+"'"
        cr.execute(sm)
        rsmember=cr.fetchone()
        print('td ', td)
        maincart = request.session['cart']
        storeids=[]
        totalstorebills=[]
        msg = "order placed successfully total bill Rs " + str(totalbill)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=harpreetsinghj&password=IMM1PVNW&message=" + msg + "&phone_numbers=" +
                      str(rsmember[3]))
        response = conn1.getresponse()
        print(response.read())
        for each in maincart:
             if each['storeid'] not in storeids:
                 storeids.append(each['storeid'])
        for sid  in storeids:
            tb=0
            for row in maincart:
                if sid == row['storeid']:
                    tb=tb+float(row['totalprice'])
            totalstorebills.append(tb)
            query1 = "insert into bill values(NULL,'" + str(td) + "','" + modeofbill + "','" + str(tb) + "','" + str(
                memberid) + "','" + str(sid) + "','online')"
            print('my q', query1)
            cr.execute(query1)
            conn.commit()
            s = "select * from bill"
            cr.execute(s)
            rs = cr.fetchall()
            orderid = ""
            for row in rs:
                orderid = row[0]
            x = request.session['cart']
            for item in maincart:
                if sid == item['storeid']:
                    query2 = "insert into billdetail values(NULL,'" + str(item['pid']) + "','" + str(
                        item['priceafterdiscount']) + "','" + str(item['quantity']) + "','" + str(orderid) + "')"
                    cr.execute(query2)
                    conn.commit()
        del request.session['cart']
        del request.session['cartsize']
        list = []
        list.append(x)
        list.append(totalbill)
        list.append(address)
        list.append(rsmember[3])
        list.append(rsmember[1])
        return render(request, 'payment successfull.html', {"data": list})
    else:
        return HttpResponseRedirect('openuserdashboard')


def fetchorders(request):
    if request.session.has_key('MEMBERID'):
        memberid = request.session['MEMBERID']
        conn = myconnection.connect('')
        cr = conn.cursor()
        query = "select * from bill where memberid='" + str(memberid) + "'"
        cr.execute(query)
        result = cr.fetchall()
        list = []
        for row in result:
            list.append(row)
        return JsonResponse(list, safe=False)

    else:
        return HttpResponseRedirect('memberlogin')

def orderdetail(request):
    orderid = request.GET['orderid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from billdetail where billid='" + str(orderid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    serialno=1
    totalprice=0
    for row in result:
        d={}
        d['serialno']=serialno
        d['detailid']=row[0]
        d['pid'] = row[1]
        q2="select * from products where productid='"+str(row[1])+"'"
        cr.execute(q2)
        pname=cr.fetchone()
        d['pname']=pname[1]
        d['brand']=pname[5]
        d['cname'] = pname[6]
        d['price'] = row[2]
        d['qty'] = row[3]
        d['billid']=row[4]
        totalprice=totalprice+((float)(row[2])*(int)(row[3]))
        d['total']=((float)(row[2])*(int)(row[3]))
        x.append(d)
        serialno=serialno+1
    list=[]
    list.append(x)
    list.append(totalprice)
    request.session['page'] = 'orderdetail'

    return render(request,'orderdetail.html',{"data":list})

def getallproducts(request):
    conn = myconnection.connect('')
    s = "select DISTINCT title from stores"
    cr = conn.cursor()
    cr.execute(s)
    res = cr.fetchall()
    conn.commit()
    print(res)
    x = []
    for row in res:
        x.append(row[0])
    return JsonResponse(x, safe=False)
def gotoproductdetailfromhome(request):
    if request.session.has_key('MEMBERID'):
        conn = myconnection.connect('')
        cr = conn.cursor()
        x = []
        s = "select * from stores"
        cr.execute(s)
        result = cr.fetchall()
        for p in result:
            d = {}
            d['storeid'] = p[0]
            d['title'] = p[1]
            x.append(d)
        request.session['page'] = 'userdashboard'
        return render(request, 'memberhome.html', {'mydata': x})
    else:
        return HttpResponseRedirect('memberlogin')

def openstoresellstock(request):
    print()
    if request.session.has_key('STOREID'):
        return render(request, 'storesellstock.html')

    else:
        return HttpResponseRedirect('storelogin')

def openstoreviewreport(request):
    print()
    if request.session.has_key('STOREID'):
        return render(request, 'storeviewreport.html')
    else:
        return HttpResponseRedirect('storelogin')

def verifymember(request):
    memberid=request.GET['memberid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    q="select * from members where memberid='"+str(memberid)+"'"
    cr.execute(q)
    result=cr.fetchone()
    print('ddddddddddddddd')
    if result==None:
        return HttpResponse('fail')
    else:
        return HttpResponse('success')

def verifyproduct(request):
    pid = request.GET['pid']
    qty = request.GET['qty']
    conn = myconnection.connect('')
    cr = conn.cursor()
    q = "select * from products where productid='" + str(pid) + "'"
    cr.execute(q)
    result = cr.fetchone()
    list = []
    price=result[2]
    afterdiscount=result[3]
    name=result[1]
    totalprice=(float)(qty)*(float)(afterdiscount)
    list.append(pid)
    list.append(name)
    list.append(qty)
    list.append(price)
    list.append(afterdiscount)
    list.append(totalprice)
    list.append(result[7])
    return JsonResponse(list, safe=False)

def sellstock(request):
    if request.session.has_key('STOREID'):
        print('')
        pricestring = list(str(request.GET['pricestring']).split(','))
        pricestringf = []
        for r in pricestring:
            if r != "":
                pricestringf.append(r)
        pidstring = list(str(request.GET['pidstring']).split(','))
        pidstringf = []
        for r in pidstring:
            if r != "":
                pidstringf.append(r)
        qtystring = list(str(request.GET['qtystring']).split(','))
        qtystringf = []
        for r in qtystring:
            if r != "":
                qtystringf.append(r)
        print(qtystringf)
        memberid = request.GET['memberid']
        totalbill = request.GET['totalbill']
        conn = myconnection.connect('')
        cr = conn.cursor()
        td = date.today()
        query1 = "insert into bill values(NULL,'" + str(td) + "','OFFLINE','" + str(totalbill) + "','" + str(
            memberid) + "','" + str(request.session['STOREID']) + "','online')"
        cr.execute(query1)
        conn.commit()
        s = "select * from bill"
        cr.execute(s)
        rs = cr.fetchall()
        orderid = ""
        for row in rs:
            orderid = row[0]
        count = 0
        for item in pidstringf:
            query2 = "insert into billdetail values(NULL,'" + str(item) + "','" + str(
                pricestringf[count]) + "','" + str(qtystringf[count]) + "','" + str(orderid) + "')"
            cr.execute(query2)
            conn.commit()
            count = count + 1

        return HttpResponse('success')
    else:
        return HttpResponseRedirect('storelogin')





def fetchordersstore(request):
    if request.session.has_key('STOREID'):
        storeid = request.session['STOREID']
        conn = myconnection.connect('')
        cr = conn.cursor()
        query = "select * from bill where storeid='" + str(storeid) + "'"
        cr.execute(query)
        result = cr.fetchall()
        list = []
        for row in result:
            list.append(row)
        return JsonResponse(list, safe=False)
    else:
        return HttpResponseRedirect('storelogin')



def orderdetailstore(request):
    orderid = request.GET['orderid']
    conn = myconnection.connect('')
    cr = conn.cursor()
    query = "select * from billdetail where billid='" + str(orderid) + "'"
    cr.execute(query)
    result = cr.fetchall()
    x = []
    serialno=1
    totalprice=0
    for row in result:
        d={}
        d['serialno']=serialno
        d['detailid']=row[0]
        d['pid'] = row[1]
        q2="select * from products where productid='"+str(row[1])+"'"
        cr.execute(q2)
        pname=cr.fetchone()
        d['pname']=pname[1]
        d['brand']=pname[5]
        d['cname'] = pname[6]
        d['price'] = row[2]
        d['qty'] = row[3]
        d['billid']=row[4]
        totalprice=totalprice+((float)(row[2])*(int)(row[3]))
        d['total']=((float)(row[2])*(int)(row[3]))
        x.append(d)
        serialno=serialno+1
    list=[]
    list.append(x)
    list.append(totalprice)
    return render(request,'reportdetail.html',{"data":list})

def openstorechangepass(request):
    if request.session.has_key('STOREID'):
        return render(request, 'storechangepassword.html')
    else:
        return HttpResponseRedirect('storelogin')

def changestorepassword(request):
    oldpass = request.POST['oldpass']
    newpass = request.POST['newpass']
    conn = myconnection.connect('')
    cr = conn.cursor()
    email=""
    if request.session.has_key('STOREEMAIL'):
        email = request.session['STOREEMAIL']
        query = "select * from stores where emailid='" + email + "' and password='" + oldpass + "'"
        cr.execute(query)
        result = cr.fetchone()
        if result == None:
            return render(request, 'storechangepassword.html', {"message": 'old password not match!!'})
        else:
            query = "update stores set password='" + newpass + "' where emailid='" + email + "'"
            cr.execute(query)
            conn.commit()
            return render(request, 'storechangepassword.html', {"message": 'password changed successfully!!'})
    else:
        return HttpResponseRedirect('storelogin')
def openmemberchangepass(request):
    if request.session.has_key('MEMBERID'):
        request.session['page'] = 'vieworders'
        return render(request, 'memberchangepassword.html')
    else:
        return HttpResponseRedirect('memberlogin')

def changememberpassword(request):
    oldpass = request.POST['oldpass']
    newpass = request.POST['newpass']
    conn = myconnection.connect('')
    cr = conn.cursor()
    email=""
    if request.session.has_key('MEMBEREMAIL'):
        email = request.session['MEMBEREMAIL']
        query = "select * from members where email='" + email + "' and password='" + oldpass + "'"
        cr.execute(query)
        result = cr.fetchone()
        if result == None:
            return render(request, 'memberchangepassword.html', {"message": 'old password not match!!'})
        else:
            query = "update members set password='" + newpass + "' where email='" + email + "'"
            cr.execute(query)
            conn.commit()
            return render(request, 'memberchangepassword.html', {"message": 'password changed successfully!!'})
    else:
        return HttpResponseRedirect('memberlogin')
from random import randint
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendotponphone(request):
    mobile=request.GET['mobile']
    # otp=random_with_N_digits(6)

    otp=random_with_N_digits(6)
    print(otp)
    msg = "your otp is " + str(otp)
    msg = msg.replace(" ", "%20")
    conn1 = http.client.HTTPConnection("server1.vmm.education")
    conn1.request('GET',
                  "/VMMCloudMessaging/AWS_SMS_Sender?username=harpreetsinghj&password=IMM1PVNW&message=" + msg + "&phone_numbers=" +
                  str(mobile))
    response = conn1.getresponse()
    print(response.read())
    return HttpResponse(otp)

def sendpassmember(request):
    mobile=request.GET['mobile']
    conn = myconnection.connect('')
    cr = conn.cursor()
    q="select * from members where mobile='"+mobile+"'"
    cr.execute(q)
    rs=cr.fetchone()
    if rs==None:
        return HttpResponse('fail')
    else:
        password = rs[5]
        msg = "your password is " + str(password)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=harpreetsinghj&password=IMM1PVNW&message=" + msg + "&phone_numbers=" +
                      str(mobile))
        response = conn1.getresponse()
        print(response.read())
        return HttpResponse('success')

def sendpassstore(request):
    mobile=request.GET['mobile']
    conn = myconnection.connect('')
    cr = conn.cursor()
    q="select * from stores where mobilenumber='"+mobile+"'"
    cr.execute(q)
    rs=cr.fetchone()
    if rs==None:
        return HttpResponse('fail')
    else:
        password = rs[3]
        msg = "your password is " + str(password)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=harpreetsinghj&password=IMM1PVNW&message=" + msg + "&phone_numbers=" +
                      str(mobile))
        response = conn1.getresponse()
        print(response.read())
        return HttpResponse('success')

def sendpassadmin(request):
    mobile=request.GET['mobile']
    conn = myconnection.connect('')
    cr = conn.cursor()
    q="select * from admin where mobile='"+mobile+"'"
    cr.execute(q)
    rs=cr.fetchone()
    if rs==None:
        return HttpResponse('fail')
    else:
        password = rs[1]
        msg = "your password is " + str(password)
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',
                      "/VMMCloudMessaging/AWS_SMS_Sender?username=harpreetsinghj&password=IMM1PVNW&message=" + msg + "&phone_numbers=" +
                      str(mobile))
        response = conn1.getresponse()
        print(response.read())
        return HttpResponse('success')

def demo(request):
    return render(request,'demo.html')

