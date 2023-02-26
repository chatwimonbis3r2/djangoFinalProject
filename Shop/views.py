import os
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from Shop.forms import CustomersForm, EmployeesForm, ProductsForm, ProductsTypeForm, RejectForm, TranfersForm, SendForm, \
    CancelForm
from Shop.models import *

def chkPermission(request):
    if 'userStatus' in request.session:
        userStatus = request.session['userStatus']
        if userStatus == 'customer':
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True
    else:
        if Employees.objects.count() != 0:
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True

def Home(request):
    countEmp = Employees.objects.count()
    print("countEmp:" + str(countEmp))
    if countEmp == 0:
        messages.add_message(request, messages.INFO, "เพิ่มข้อมูลพนักงาน สำหรับการเข้าใช้ครั้งแรก")
        return redirect('EmpSignUp')
    else:
        return render(request, 'Front/Home.html')

def SignUp(request):
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']
            if password == confirmPassword:
                form.save()
                # สร้าง user ในระบบ authen ของ Django ---
                cid = request.POST['cid']
                name = request.POST['name']
                email = 'none@gmail.com'
                password = request.POST['password']
                user = User.objects.create_user(cid, email, password)
                user.first_name = name
                user.is_staff = False
                user.save()
                # -------
                return redirect('SignIn')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านกับรหัสผ่านที่ยืนยันไม่ตรงกัน...")
                context = {'form': form}
                return render(request,'Login-Logout/SignUp.html',context)
        else:
            messages.add_message(request, messages.WARNING, "ป้อนข้อมูลไม่ถูกต้อง ไม่สมบูรณ์...")
            context = {'form': form}
            return render(request,'Login-Logout/SignUp.html',context)
    else:
        form = CustomersForm()
        context = {'form': form}
        return render(request,'Login-Logout/SignUp.html',context)

def EmpSignUp(request):
    if not chkPermission(request):
        return redirect('Home')
    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            # สร้าง user ในระบบ authen ของ Django ---
            eid = request.POST['eid']
            name = request.POST['name']
            email = 'none@gmail.com'
            password = request.POST['password']
            user = User.objects.create_user(eid, email, password)
            user.first_name = name
            user.is_staff = True
            user.save()
            # -------
            return redirect('Home')
        else:
            context = {'form': form}
            return render(request,'Login-Logout/EmpSignUp.html',context)
    else:
        form = EmployeesForm()
        context = {'form': form}
        return render(request,'Login-Logout/EmpSignUp.html',context)

def SignIn(request):
    if request.method == 'POST':
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")
        ## login ด้วย ระบบล็อกอินของ Django
        user = authenticate(username=userName, password=userPass)
        if user is not None:
            login(request, user)
            if user.is_staff == 0:
                user = Customers.objects.get(cid=userName)
                request.session['userId'] = user.cid
                request.session['userName'] = user.name
                request.session['userStatus'] = 'customer'
                messages.add_message(request, messages.INFO, "เข้าสู่ระบบสำเร็จ..")
            else:
                emp = Employees.objects.get(eid=userName)
                request.session['userId'] = emp.eid
                request.session['userName'] = emp.name
                request.session['userStatus'] = emp.position
                messages.add_message(request, messages.INFO, "เข้าสู่ระบบสำเร็จ..")
            if request.session.get('orderActive'):
                del request.session['orderActive']
                return redirect('checkout')
            else:
                return redirect('Home')
        else:
            messages.error(request, "User Name or Password not correct..!!!")
            data = {'userName': userName}
            return render(request,'Login-Logout/SignIn.html',data)
    else:
        data = {'userName': ''}
        return render(request,'Login-Logout/SignIn.html',data)

def SignOut(request):
    del request.session["userId"]
    del request.session["userName"]
    del request.session["userStatus"]
    logout(request)
    return redirect('Home')

@login_required(login_url='SignIn')
def ProductTypeList(request):
    ProductsTypeList = ProductsType.objects.all()
    context = {'ProductType':ProductsTypeList}
    return render(request, 'Back/ProductType/ProductTypeList.html',context)
@login_required(login_url='SignIn')
def ProductTypeNew(request):
    if request.method == 'POST':
        form = ProductsTypeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, messages.SUCCESS,"เพิ่มข้อมูลสำเร็จ")
            return redirect('ProductTypeList')
        else:
            context = {'form': form}
            messages.error(request, messages.ERROR,"เพิ่มข้อมูลไม่สำเร็จ")
            return render(request, 'Back/ProductType/ProductTypeNew.html', context)
    else:
        form = ProductsTypeForm()
    context = {'form': form}
    return render(request, 'Back/ProductType/ProductTypeNew.html',context)
@login_required(login_url='SignIn')
def ProductTypeEdit(request,id):
    ProductType = ProductsType.objects.get(id=id)
    obj = get_object_or_404(ProductsType, id=id)
    form = ProductsTypeForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'แก้ไขสำเร็จ')
            return redirect('ProductTypeList')
        else:
            messages.add_message(request, messages.WARNING,'แก้ไขไม่สำเร็จ')
            return render(request, 'Back/ProductType/ProductTypeEdit.html')
    form.ProductsTypeEditForm()
    context = {'form': form}
    return render(request, 'Back/ProductType/ProductTypeEdit.html',context)
@login_required(login_url='SignIn')
def ProductTypeDelete(request,id=None):
    if request.method == 'POST':
        id = request.POST['id']
        ProductTypes = ProductsType.objects.get(id=id)
        if ProductTypes:
            ProductTypes.delete()
            messages.add_message(request, messages.SUCCESS, 'ลบสำเร็จ')
            return redirect('ProductTypeList')
        else:
            messages.add_message(request, messages.WARNING, 'ลบไม่สำเร็จ')
    else:
        ProductTypes = ProductsType.objects.get(id=id)
    context = {'ProductType': ProductTypes}
    return render(request, 'Back/ProductType/ProductTypeDelete.html',context)
@login_required(login_url='SignIn')
def ProductList(request):
    ProductList = Products.objects.all()
    context = {'Products': ProductList}
    return render(request, 'Back/Product/ProductList.html',context)
@login_required(login_url='SignIn')
def ProductNew(request):
    if request.method == 'POST':
        form = ProductsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'บันทึกเรียบร้อย')
            return redirect('ProductList')
        else:
            Product = get_object_or_404(Products,pid=request.POST['pid'])
            if Product:
                messages.add_message(request, messages.WARNING, "รหัสสินค้าซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'Back/Product/ProductNew.html', context)
    else:
        form = ProductsForm()
        context = {'form': form}
        return render(request, 'Back/Product/ProductNew.html',context)
@login_required(login_url='SignIn')
def ProductEdit(request,pid):
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name
    if request.method == 'POST':
        form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            pid = newForm.pid
            print(newForm.picture.name)
            if newForm.picture.name != picture:
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = pid + ext
                product = get_object_or_404(Products, pid=pid)
                product.picture.name = '/products/' + newfilename
                product.save()
                if os.path.exists('static/products/' + newfilename):
                    os.remove('static/products/' + newfilename)
                os.rename('static/products/' + filename, 'static/products/' + newfilename)
            else:
                newForm.save()
        return redirect('ProductList')
    else:
        form = ProductsForm(instance=product)
        form.ProductsEditForm()
        context = {'form': form}
    return render(request, 'Back/Product/ProductEdit.html',context)
@login_required(login_url='SignIn')
def ProductDelete(request,pid):
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name
    if request.method == 'POST':
        product.delete()
        if os.path.exists('static' + picture):
            os.remove('static' + picture)
        return redirect('SignIn')
    else:
        form = ProductsForm(instance=product)
        form.ProductsDeleteForm()
        context = {'form': form, 'Product': product}
        return render(request, 'Back/Product/ProductDelete.html',context)
@login_required(login_url='SignIn')
def CustomerList(request):
    CustomerList = Customers.objects.all()
    context = {'Customers': CustomerList}
    return render(request, 'Back/Customer/CustomerList.html',context)
@login_required(login_url='SignIn')
def CustomerNew(request):
    if request.method == 'POST':
        form = CustomersForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'เพิ่มข้อมูลสำเร็จ')
            return redirect('CustomerList')
        else:
            Customer = get_object_or_404(Customers,pid=request.POST['pid'])
            if Customer:
                messages.add_message(request, messages.WARNING, "รหัสซ้ำที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'Back/Customer/CustomerNew.html', context)
    else:
        form = CustomersForm()
        context = {'form': form}
        return render(request, 'Back/Customer/CustomerNew.html',context)
@login_required(login_url='SignIn')
def CustomerEdit(request,cid):
    Customer = Customers.objects.get(cid=cid)
    obj = get_object_or_404(Customers, cid=cid)
    form = CustomersForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขสำเร็จ')
            return redirect('CustomerList')
        else:
            messages.add_message(request, messages.WARNING, 'แก้ไขไม่สำเร็จ')
            return render(request, 'Back/Customer/CustomerEdit.html')
    form.CustomerEditForm()
    context = {'form': form}
    return render(request, 'Back/Customer/CustomerEdit.html',context)
@login_required(login_url='SignIn')
def CustomerDelete(request,cid):
    if request.method == 'POST':
        cid = request.POST['cid']
        Customer = Customers.objects.get(cid=cid)
        if Customer:
            Customer.delete()
            messages.add_message(request, messages.SUCCESS, 'ลบสำเร็จ')
            return redirect('CustomerList')
        else:
            messages.add_message(request, messages.WARNING, 'ลบไม่สำเร็จ')
    else:
        Customer = Customers.objects.get(cid=cid)
    context = {'Customer': Customer}
    return render(request, 'Back/Customer/CustomerDelete.html', context)
@login_required(login_url='SignIn')
def EmployeeList(request):
    EmployeeList = Employees.objects.all()
    context = {'Employees': EmployeeList}
    return  render(request,'Back/Employee/EmployeeList.html',context)
@login_required(login_url='SignIn')
def EmployeeNew(request):
    if request.method == 'POST':
        form = EmployeesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'เพิ่มข้อมูลสำเร็จ')
            return redirect('EmployeeList')
        else:
            Employee = get_object_or_404(Employees,eid=request.POST['eid'])
            if Employee:
                messages.add_message(request, messages.WARNING, "รหัสซ้ำที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request,'Back/Employee/EmployeeNew.html',context)
    else:
        form = EmployeesForm()
        context = {'form': form}
        return render(request,'Back/Employee/EmployeeNew.html',context)
@login_required(login_url='SignIn')
def EmployeeEdit(request,eid):
    Employee = Employees.objects.get(eid=eid)
    obj = get_object_or_404(Employees, eid=eid)
    form = EmployeesForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขสำเร็จ')
            return redirect('EmployeeList')
        else:
            messages.add_message(request, messages.WARNING, 'แก้ไขไม่สำเร็จ')
    form.EmployeeEditForm()
    context = {'form': form}
    return render(request,'Back/Employee/EmployeeEdit.html',context)
@login_required(login_url='SignIn')
def EmployeeDelete(request,eid):
    if request.method == 'POST':
        eid = request.POST['eid']
        Employee = Employees.objects.get(eid=eid)
        if Employee:
            Employee.delete()
            messages.add_message(request, messages.SUCCESS, 'ลบสำเร็จ')
            return redirect('EmployeeList')
        else:
            messages.add_message(request, messages.WARNING, 'ลบไม่สำเร็จ')
    else:
        Employee = Employees.objects.get(eid=eid)
    context = {'Employee': Employee}
    return render(request,'Back/Employee/EmployeeDelete.html',context)

def Shop(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(pid)
            if quantity:
                cart[pid] = quantity + qnt
            else:
                cart[pid] = qnt
        else:
            cart = {}
            cart[pid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('Shop')
    else:
        ProductList = Products.objects.all().order_by('pid')
        context = {'Products': ProductList}
        return render(request, 'Front/Shop.html', context)

@login_required(login_url='SignIn')
def Basket(request):
    cart = request.session.get('cart')
    if request.method == 'POST':
        action = request.POST.get('action')
        pid = request.POST.get('pid')
        qnt = int(request.POST.get('qnt'))
        if action=="Update": #กดปุ่ม Update
            if cart[pid]:
                cart[pid] = qnt
        else: # กดปุ่มลบ
            del cart[pid]
        request.session['cart'] = cart
        request.session['count'] = len(cart)
    if len(cart) == 0:
        del request.session['cart']
        del request.session['count']
        del request.session['sum']
        return redirect('Shop')
    cart = request.session.get('cart')
    items = []
    sum=0.00
    for item in cart:
        product = Products.objects.get(pid=item)
        total=product.price * cart[item]
        sum+=total
        items.append({'product':product, 'quantity':cart[item], 'total':total})
    request.session['sum'] = sum
    data={'items':items}
    return render(request, 'Front/Basket.html',data)

@login_required(login_url='SignIn')
def ClearBasket(request):
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return redirect('Shop')

@login_required(login_url='SignIn')
def CartSutmit(request):
    cart = request.session.get('cart')
    items = []
    sum = 0.00
    if cart:
        if not request.session.get('userId'):
            request.session['orderActive'] = True
            return redirect('userAuthen')
        cart = request.session.get('cart')
        date = datetime.now()
        # print("date:", date)
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        order = Orders()
        order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
        order.customer = customer
        for item in cart:
            # print(item, cart[item])
            product = Products.objects.get(pid=item)
            total = product.price * cart[item]
            sum += total
            items.append({'product': product, 'quantity': cart[item], 'total': total})
        request.session['sum'] = sum
        data = {'items': items, 'order': order}
        return render(request, 'Front/CartSubmit.html', data)
    else:
        messages.add_message(request, messages.WARNING, "No product in basket!!!..")
        return redirect('Shop')
@login_required(login_url='SignIn')
def SubmitOrder(request):
    cart = request.session.get('cart')
    if cart is None:
        return redirect('Shop')
    items = []
    date = datetime.now()
    customer = get_object_or_404(Customers, cid=request.session.get('userId'))
    order = Orders()
    order.newOrderId()
    order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
    order.customer = customer
    order.status = "1"
    order.save()
    for item in cart:  # get any key from cart
        product = Products.objects.get(pid=item)
        quantity = cart[item]
        total = product.price * cart[item]
        orderDetail = OrderDetails()
        orderDetail.order = order
        orderDetail.product = product
        orderDetail.oprice = product.price
        orderDetail.quantity = quantity
        orderDetail.save()
        items.append({'product': product, 'quantity': cart[item], 'total': total})
    count = request.session.get('count')
    sum = request.session.get('sum')
    data = {'items': items, 'order': order, 'count': count, 'sum': sum}
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return render(request, 'Front/SubmitOrder.html', data)

def ViewOrder(request):
    orders = []
    if request.session.get("userStatus") == 'customer':
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        orders = None
        if customer:
            orders = Orders.objects.filter(customer=customer).order_by('odate').reverse()
        context = {'customer': customer, 'orders': orders}
        return render(request, 'Front/ViewOrder.html', context)
    else:  # employee
        orders = Orders.objects.filter(~Q(status='5')).exclude(status='6').exclude(status='7').order_by(
            'odate').reverse()  # อ่านใบสั่งซื้อที่ status 1-4
        context = {'orders': orders}
        return render(request, 'Front/ViewOrder.html', context)

def DetailOrder(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    if request.method == 'POST':
        return redirect('Home')
    else:
        context = {'order': order}
        return render(request, 'Front/DetailOrder.html', context)

@login_required(login_url='SignIn')
def OrderConfirm(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get('userId'))
    confirm = Confirms()
    confirm.order = order
    confirm.employee = employee
    confirm.save()
    order.status = '2'
    order.save()
    return redirect('ViewOrder')

@login_required(login_url='SignIn')
def OrderReject(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get("userId"))
    form = RejectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '7'
            order.save()
        return redirect('ViewOrder')
    else:
        form = RejectForm(initial={'order': order, 'employee': employee})
        context = {'form': form, 'order': order}
        return render(request, 'Front/OrderReject.html', context)

@login_required(login_url='SignIn')
def MoneyTransfer(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = TranfersForm(request.POST or None, files=request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status='3'
            order.save()
        return redirect('ViewOrder')
    else:
        form = TranfersForm(initial={'order':order})
        context = {'form':form, 'order':order }
        return render(request, 'Front/MoneyTransfer.html', context)

@login_required(login_url='SignIn')
def MoneyAccept(request,oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get('userId'))
    accept = Accepts()
    accept.order = order
    accept.employee = employee
    accept.save()
    order.status = '4'
    order.save()
    return redirect('ViewOrder')

@login_required(login_url='SignIn')
def ProductSend(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get("userId"))
    form = SendForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '5'
            order.save()
        return redirect('ViewOrder')
    else:
        form = SendForm(initial={'order': order, 'employee':employee})
        context = {'form': form, 'order': order}
        return render(request, 'Front/ProductSend.html', context)

@login_required(login_url='SignIn')
def OrderCancel(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = CancelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '6'
            order.save()
        return redirect('ViewOrder')
    else:
        form = CancelForm(initial={'order': order})
        context = {'form': form, 'order': order}
        return render(request, 'Front/OrderCancel.html', context)

@login_required(login_url='SignIn')
def Dashboard(request):
    ProductsAll = Products.objects.all()
    ProductCount = len(ProductsAll)
    CustomerAll = Customers.objects.all()
    CustomerCount = len(CustomerAll)
    EmployeesAll = Employees.objects.all()
    EmployeesCount = len(EmployeesAll)
    OrdersAll = Orders.objects.all()
    OrdersCount = len(OrdersAll)
    context = {"ProductCount": ProductCount,
               "CustomerCount": CustomerCount,
               "EmployeesCount": EmployeesCount,
               "OrdersCount": OrdersCount,}
    return render(request, 'Back/Dashboard.html',context)

