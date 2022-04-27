from turtle import home
from django.shortcuts import render, HttpResponse


from dataclasses import dataclass
from django.http import HttpResponse
from django.shortcuts import render

import pymysql.cursors
import pymysql
import json

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def connection():
    dataBase = pymysql.connect(
        host='bcgy7zqwn3xsrqrlzlqc-mysql.services.clever-cloud.com',
        user='uglv1cpvawucauko',
        password='Sa1Hnp8Wibs4usc0e4CD',
        db='bcgy7zqwn3xsrqrlzlqc',
        autocommit=True
    )
    return dataBase


db = connection()


def index(request):

	if request.session['type'] == 'Customer':
		return redirect('customer')

	if request.session['type'] == 'Delivery':
		return redirect('delivery')

	if request.session['type'] == 'Seller':
		return redirect('seller')

	return render(request,'home.html')


def handleLogout(request):
    try:
        del request.session['email']
        del request.session['type']
    except:
        return redirect('handleLogin')

    return redirect('handleLogin')


def handleLogin(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        loginAs = request.POST.get('user')

        user = authenticate(username=(
            email+loginAs), password=password, first_name=email, last_name=loginAs)

        print(type(user))
        if user is not None:
            login(request, user)
            if(loginAs == 'Seller'):

                request.session['email'] = email
                request.session['type'] = loginAs
                return redirect('seller')

            if(loginAs == 'Customer'):
                request.session['email'] = email
                request.session['type'] = loginAs
                return redirect('customer')

            if(loginAs == 'Delivery'):
                request.session['email'] = email
                request.session['type'] = loginAs
                return redirect('delivery')
        else:
            messages.error(request, 'Please check Login details')
            return redirect('handleLogin')

    return render(request, "login.html")


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('firstName')
        phone = request.POST.get('phoneNumber')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        signAs = request.POST.get('user')

        if(len(email) < 4):
            messages.error(request, 'Email length must be 4')
            return redirect('signup')
        elif(len(name) < 2):

            messages.error(
                request, 'firstName must be greater than 2 characters')

            return redirect('signup')
        elif (password1 != password2):

            messages.error(request, 'Password dont match')

            return redirect('signup')
        elif(len(password1) < 5):
            messages.error(request, 'Password must be 5 characters')

            return redirect('signup')

        db.ping()
        cur = db.cursor()

        if(signAs == "Customer"):
            cur.execute(
                "INSERT INTO customer(customerName,customerNumber,customerEmail) VALUES(%s,%s,%s)", (name, phone, email))

            val = cur.execute("SELECT * FROM customer")
            print(cur.fetchall())
        elif(signAs == "Seller"):
            print("+++++++++++++++++++++++++++++++++++++++++++")
            cur.execute(
                "INSERT INTO seller(sellerEmail,sellerName,sellerNumber,sellerWarehouse) VALUES(%s,%s,%s,%s)", (email, name, phone, 1))
            print("--------------------------------------------")
            val = cur.execute("SELECT * FROM seller")
            print(cur.fetchall())
        elif(signAs == "Delivery"):
            cur.execute(
                "INSERT INTO delivery(deliveryName,deliveryNumber,deliveryEmail) VALUES(%s,%s,%s)", (name, phone, email))
        else:
            return HttpResponse("<h1>Invalid</h1>")

        usname = email+signAs

        myuser = User.objects.create_user(usname, email, password1)
        myuser.save()
        messages.success(request, 'Account created')

        return redirect('handleLogin')

    return render(request, "signup.html")


def add_product(request):
    if request.method == 'POST':
        productID = request.POST.get('productID')
        ProductName = request.POST.get('ProductName')
        category = request.POST.get('category')
        Price = request.POST.get('Price')
        Brand = request.POST.get('Brand')
        sellerEmail = request.POST.get('Seller ID')
        img = request.FILES.get('filename')
        print(img, type(img))
        bin_img = img.read()
        print(type(img.file), type(bin_img))

        db.ping()
        cur = db.cursor()
        cur.execute("INSERT INTO Product(ProductID,ProductName,Price,Brand,CategoryID,sellerEmail,image) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (productID, ProductName, Price, Brand, category, sellerEmail, bin_img))

        return redirect('seller')

    return render(request, 'add_Product.html')


def seller(request):

    sellerEmail = request.session['email']
    if request.method == 'POST' and 'add_product' in request.POST:
        return redirect('add_product')
    if request.method == 'POST' and 'drop_product' in request.POST:
        productID = request.POST['productID']
        db.ping()
        cur = db.cursor()

        print(productID, "-----------")
        cur.execute("DELETE FROM Product WHERE sellerEmail= %(seller_id)s AND ProductID=%(proId)s", {
                    'seller_id': sellerEmail, 'proId': productID})
        return redirect('seller')

    if request.method == 'POST' and 'update_price' in request.POST:
        db.ping()
        cur = db.cursor()
        productID = request.POST['productID']
        update_Price = request.POST.get('Update Price')
        cur.execute("UPDATE Product SET Price = %(newprice)s WHERE  productID = %(proId)s AND sellerEmail=%(seller_id)s", {
                    'newprice': update_Price, 'seller_id': sellerEmail, 'proId': productID})
        # query=f"UPDATE Product SET Price = {update_Price} WHERE  productID = {productID} AND sellerEmail={sellerEmail};"
        return redirect('seller')

    db.ping()
    cur = db.cursor()
    # cur.execute("Select * from Customer")
    cur.execute("Select ProductID,ProductName,Price,Brand,CategoryID from Product where sellerEmail=%(seller_id)s", {
                'seller_id': sellerEmail})
    table = cur.fetchall()

    cur = db.cursor()
    # cur.execute("Select * from Customer")
    cur.execute("Select ProductID,OrderID, Quantity from Inventory where sellerEmail=%(seller_id)s", {
                'seller_id': sellerEmail})
    table1 = cur.fetchall()
    return render(request, 'Seller.html', {'table': table, 'table1': table1})


def delivery(request):
    print(request.session['email'])
    return render(request, 'delivery.html')


# newly added

def customer(request):
    return render(request, 'customer.html')


def electronics(request):

    db.ping()
    cur = db.cursor()
    cur.execute("select * from Product where categoryID=2")
    output = cur.fetchall()
    print(request.session['email'])
<<<<<<< HEAD


    for i in range(len(output)):
        # binary_data = base64.b64decode(output[0][6])

        print((output[i][6]))
        print('-------------------------------------------------------------------')
        if(output[i][6] == None ):
            continue


        image = Image.open(io.BytesIO(output[i][6]))


        print(io.BytesIO(output[i][6]))
        image = image.convert('RGB')
        image.save('static/' + str(i) + '_electronics' + '.jpeg')

    for i in range(len(output)):
        output = [output[i] + tuple(['static/' + str(i) + '_electronics' + '.jpeg' ]) for i in range(len(output))]

    return render(request, 'electronics.html', {'products': output})


def clothing(request):
    db.ping()
    cur = db.cursor()
    cur.execute("select * from Product where categoryID=1")
    output = cur.fetchall()

    return render(request, 'clothing.html', {'products': output})


def groceries(request):
    db.ping()
    cur = db.cursor()
    cur.execute("select * from Product where categoryID=3")
    output = cur.fetchall()

    return render(request, 'groceries.html', {'products': output})


def checkout(request):
    db.ping()
    my_cursor2 = db.cursor()
    Cid = request.session['email']
    my_cursor2.execute(
        "select ProductID,sellerEmail,price,quantity from cart where customerEmail= %(Cid)s", {'Cid': Cid})
    output = my_cursor2.fetchall()

    ProductID = [O[0] for O in output]
    sellerEmail = [O[1] for O in output]
    price = [O[2] for O in output]
    quantity = [O[3] for O in output]

    output = []
    amt = 0
    for i in range(len(ProductID)):
        my_cursor2.execute("Select * from Product Where ProductID =  %(Pro_id)s and sellerEmail = %(Sell_id)s",
                           {'Pro_id': ProductID[i], 'Sell_id': sellerEmail[i]})
        a = my_cursor2.fetchone()
        output.append(a)
        amt = amt+price[i]
    output = [output[i] + tuple([quantity[i]]) for i in range(len(output))]

    return render(request, 'checkout.html', {'products': output, 'amt': amt, 'quantity': quantity, 'len': len(ProductID)})


def update_item(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        Pid, Sid, action = int(body['Pid']), body['Sid'], body['action']
        Cid = request.session['email']

        my_connection = connection()
        my_connection.ping()
        my_cursor = my_connection.cursor()

        quantity = 1

        # Select query
        my_cursor.execute("SELECT Price FROM Product WHERE ProductID = %(Pro_id)s AND sellerEmail = %(Sell_id)s ", {
                          'Pro_id': Pid, 'Sell_id': Sid})
        price = my_cursor.fetchone()[0]

        # Finding Quantity
        query = f'SELECT quantity FROM cart WHERE customerEmail = \'{Cid}\' AND sellerEmail = \'{Sid}\' AND ProductID = {Pid}'
        my_cursor.execute(query)
        output = my_cursor.fetchall()

        if len(output) != 0:
            quantity = output[0][0] + 1
            query = f'UPDATE cart SET quantity = {quantity}, price = {price*quantity} WHERE customerEmail = \'{Cid}\' AND sellerEmail = \'{Sid}\' AND ProductID = {Pid}'
        else:
            query = f'INSERT INTO cart(customerEmail,sellerEmail,ProductID,quantity,price) VALUES(\'{Cid}\',\'{Sid}\',{Pid},{quantity},{price*quantity})'

        my_cursor.execute(query)
        my_connection.commit()

    return JsonResponse('Cart was updated', safe=False)

def create_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zip_code = request.POST.get('zip')

        Cid = request.session['email']
        my_connection = connection()
        my_connection.ping()
        my_cursor = my_connection.cursor()

        my_cursor.execute(f'SELECT * FROM cart WHERE customerEmail = \'{Cid}\'')
        cart = my_cursor.fetchall()

        

        # my_cursor.execute(f'DELETE FROM cart WHERE customerEmail = \'{Cid}\'')
        

        return redirect(customer)

    return redirect(checkout)
