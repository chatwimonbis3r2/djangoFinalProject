from datetime import datetime

from django.db import models
from django.db.models import Sum, F, Count


class Employees(models.Model):
    eid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    birthdate = models.DateField(default=None)
    position = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.eid + ":" + self.name + ", " + self.position

class Customers(models.Model):
    cid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    address = models.TextField(max_length=400, default="")
    tel = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.cid + ":" + self.name + ", " + self.tel

class ProductsType(models.Model):
    name = models.CharField(max_length=50, default="")
    desc = models.TextField(max_length=400, default="")
    def __str__(self):
        return str(self.id) + ":" + self.name

class Products(models.Model):
    pid = models.CharField(max_length=13, primary_key=True, default="")
    category = models.ForeignKey(ProductsType, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50, default="")
    net = models.IntegerField(default=0)
    price = models.FloatField(default=0.00)
    picture = models.ImageField(upload_to ='static/products/', default="")
    def __str__(self):
        return self.pid + ":" + self.name + ", " + str(self.price)

class Orders(models.Model):
    oid = models.CharField(max_length=13, primary_key=True, default="")
    odate = models.DateTimeField(auto_now_add = True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=1, default="")
    def __str__(self):
        return self.oid + " " + str(self.odate.strftime("%y-%m-%d")) + " : " + self.customer.name + ", " + str(self.getTotal()) + ", "+  self.getStatus()

    def newOrderId(self):
        #OD-yymm-xxxxx  ===> OD-2302-00001
        yy = str(datetime.today().strftime('%y'))
        mm = str(datetime.today().strftime('%m'))
        lastOrder = Orders.objects.last()
        if lastOrder:
            lastId = int(lastOrder.oid[9:])
        else:
            lastId = 0
        id = str(lastId+1)
        id=id.zfill(5)
        newId  = "OD-"+ yy + mm + "-" + id
        self.oid = newId

    def getStatus(self):
        if self.status == '1':
            return 'Wait for Confirm'
        elif self.status == '2':
            return 'Wait for Money Transfer'
        elif self.status == '3':
            return 'Wait for Money Accept'
        elif self.status == '4':
            return 'Wait for Product Send'
        elif self.status == '5':
            return 'Complete'
        elif self.status == '6':
            return 'Cancel'
        elif self.status == '7':
            return 'Reject'

    def getOrderDetails(self):
        orderDetails = OrderDetails.objects.filter(order=self)
        return orderDetails

    def getTotal(self):
        total=OrderDetails.objects.filter(order=self).aggregate(total=Sum(F('oprice') * F('quantity')))
        return total['total']

    def getCount(self):
        count= OrderDetails.objects.filter(order=self).aggregate(count=Count('id'))
        return count['count']

class OrderDetails(models.Model):
    order=models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Products, on_delete=models.CASCADE, default=None)
    oprice = models.FloatField(default=0.00)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return self.order.oid + " : " + self.product.pid + " " + self.product.name + ", " + str(self.quantity)
    def getTotal(self):
        return self.oprice * self.quantity

class Confirms(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add = True)

class Transfers(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    tdate = models.DateTimeField(auto_now_add = True)
    reference = models.CharField(max_length=35, default="")
    bank = models.CharField(max_length=50, default="")
    bill = models.ImageField(upload_to ='static/bills/', default="")

class Accepts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    adate =models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length=200, default="")

class Send(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    sdate = models.DateTimeField(auto_now_add = True)
    company = models.CharField(max_length=50, default="")
    tag = models.CharField(max_length=50, default="")
    comment = models.CharField(max_length=200, default="")

class Cancel(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, default="")

class Reject(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    rdate = models.DateTimeField(auto_now_add=True)