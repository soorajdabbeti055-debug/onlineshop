from django.shortcuts import render, redirect, get_object_or_404
from .models import shopkeeper,addproduct,signup,buy
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random


def Allhome(request):
    # Ensure the session is truly empty
    if not request.session.get('shop_email') and not request.session.get('user_email'):
        return render(request, 'allhome.html')

    elif 'shop_email' in request.session:
        prof = get_object_or_404(shopkeeper, email=request.session['shop_email'])
        product = addproduct.objects.filter(shop_id=prof)
        return render(request, 'shopprofile.html', {'prof': prof, 'product': product})

    elif 'user_email' in request.session:
        user=signup.objects.filter(email=request.session['user_email']).first()
        if user:
            shop = shopkeeper.objects.filter(district=user.district,mandal=user.mandal,village=user.village)
            return render(request, 'customermain.html',{'shop':shop})
        else:
            messages.error(request, "User not found.")
            return render(request,'allhome.html')
    
    return render(request, 'allhome.html')


def Shopkeeper(request):
    if request.method == 'POST':
        ownername = request.POST['ownername']
        shopname = request.POST['shopname']
        shoptype = request.POST['shoptype']
        shopowner = request.FILES.get('shopowner')
        shopimage = request.FILES.get('shopimage')
        district = request.POST['district']
        mandal = request.POST['mandal']
        village = request.POST['village']
        area = request.POST['area']
        number = request.POST.get('number')  # Ensure consistency with models.py
        email = request.POST['email']
        password = request.POST['password']

        # Check if shop already exists
        if shopkeeper.objects.filter(email=email).exists():
            messages.error(request, "Shop with this email already exists.")
            return render(request, 'shopkeeper.html')

        shop = shopkeeper(
            ownername=ownername, 
            shopname=shopname, 
            shoptype=shoptype, 
            shopowner=shopowner, 
            shopimage=shopimage, 
            district=district, 
            mandal=mandal, 
            village=village, 
            area=area, 
            number=number, 
            email=email, 
            password=password, # Will be hashed in `save()`
            is_open=True
        )
        shop.save()
        
        request.session['shop_email'] = shop.email
        messages.success(request, 'Shopkeeper registration successful!')
        return redirect('Shopprofile')

    return render(request, 'shopkeeper.html')

def Leaveshop(request):
    request.session.flush()  # Logs out user
    request.session.clear()
    messages.success(request, 'You have left the shop.')
    return redirect('Allhome')

def Reopenshop(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            shop = shopkeeper.objects.get(email=email,password=password)
            if shop:  # Secure password check
                request.session['shop_email'] = shop.email
                messages.success(request, 'Shop reopened successfully!')
                return redirect('Shopprofile')
            else:
                messages.error(request, 'Invalid email or password.')
        except shopkeeper.DoesNotExist:
            messages.error(request, 'Invalid emailpassword.')

    return render(request, 'reopenshop.html')  # Show login page on failure



def Addproduct(request):
    if request.method == 'POST':
        productname = request.POST['productname']
        productimageone=request.FILES.get('productimageone')
        productimagetwo=request.FILES.get('productimagetwo')
        productprice=request.POST['productprice']
        productinfo=request.POST.get('productinfo','').strip()
        shop_email = request.session.get('shop_email')
        if not shop_email:
            messages.error(request, 'Please login first.')
            return redirect('Shopkeeper')
        try:
            shop = shopkeeper.objects.get(email=shop_email)
        except shopkeeper.DoesNotExist:
            messages.error(request,'shop not found')
            return redirect('Shopkeeper')
        product = addproduct(
            shop_id=shop,
            productname=productname,
            productimageone=productimageone,
            productimagetwo=productimagetwo,
            productprice=productprice,
            productinfo=productinfo)
        product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('Shopprofile')
    return render(request, 'addproduct.html')

def Customer(request):
   return render(request, 'signup.html')

def Shopprofile(request):
    return redirect('Allhome')

def Signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        district=request.POST['district']
        mandal=request.POST['mandal']
        village=request.POST['village']
        area=request.POST['area']
        near_by=request.POST['near_by']
        h_no=request.POST['h_no']
        exists_user=signup.objects.filter(email=email).exists()
        if exists_user:
            messages.error(request, 'User already exists!')
            return redirect('Signup')
        else:
            user=signup(username=username,email=email,password=password,district=district,mandal=mandal,village=village,area=area,near_by=near_by,h_no=h_no)
            user.save()
            request.session['user_email'] = user.email
            messages.success(request, 'User added successfully!')
            return redirect('Customermain')
    return render(request, 'signup.html')

def Signin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            user=signup.objects.get(email=email,password=password)
            if user:
                request.session['user_email'] = user.email
                messages.success(request, 'User logged in successfully!')
                return redirect('Customermain')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('Allhome')
        except signup.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('Allhome')
    return render(request,'signin.html')

def Signout(request):
    request.session.flush()
    request.session.clear() 
    messages.success(request,'User signed out successfully')
    return redirect('Allhome')

def Customermain(request):
    user=signup.objects.filter(email=request.session['user_email']).first()
    if user:
        shop = shopkeeper.objects.filter(district=user.district,mandal=user.mandal,area=user.area)
        return render(request, 'customermain.html',{'shop':shop})
    else:
        messages.error(request, "User not found.")
        return render(request,'allhome.html')

def Productdetails(request,id):
    pro=get_object_or_404(addproduct,product_id=id)
    return render(request,'Productdetails.html',{'pro':pro})

def Shopproduct(request,id):
    shopproduct=addproduct.objects.filter(shop_id=id)
    return render(request,'Shopproduct.html',{'shopproduct':shopproduct})

def Shopproductdetails(request,id):
    pro=get_object_or_404(addproduct,product_id=id)
    return render(request,'Shopproductdetails.html',{'pro':pro})


import pywhatkit as kit
import time
import random

def send_whatsapp_otp(number, otp, productname):
    try:
        message = f"""🛒 Order Verification

Product: {productname}
Your OTP: {otp}

Do not share this OTP.
"""

        print("Sending WhatsApp OTP to:", number)

        kit.sendwhatmsg_instantly(
            phone_no=number,
            message=message,
            wait_time=30,     # give time to load whatsapp
            tab_close=False,
        )

        time.sleep(10
                   )
        print("OTP SENT SUCCESSFULLY")

    except Exception as e:
        print("WhatsApp sending failed:", e)
        raise e


def Buy(request, id):

    if 'user_email' not in request.session:
        messages.error(request, "You must be logged in.")
        return redirect('Signin')

    product = get_object_or_404(addproduct, product_id=id)
    user = get_object_or_404(signup, email=request.session['user_email'])

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == "send_otp":

            number = request.POST.get('number')
            quantity = int(request.POST.get('quantity', 1))
            otp = generate_otp()

            order = buy.objects.create(
                product=product,
                product_image=product.productimageone,
                user=user,
                quantity=quantity,
                number=number,
                otp=otp,
                is_verified=False
            )

            request.session['order_id'] = order.id
            order.refresh_from_db()

            try:
                send_whatsapp_otp(order.number, otp, product.productname)
                messages.success(request, f"OTP sent to WhatsApp {order.number}")
            except Exception as e:
                order.delete()
                del request.session['order_id']
                messages.error(request, "Failed to send OTP")

            return redirect('Buy', id=id)

    return render(request, 'buy.html', {'product': product})



def generate_otp():
    return str(random.randint(100000, 999999))


def VerifyOrderOTP(request):
    order_id = request.session.get('order_id')

    if not order_id:
        messages.error(request, "Session expired. Please order again.")
        return redirect('Customermain')

    order = get_object_or_404(buy, id=order_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if entered_otp == order.otp:
            order.is_verified = True
            order.otp = None
            order.save()

            del request.session['order_id']
            messages.success(request, "Order confirmed successfully!")
            return redirect('Customermain')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_order_otp.html')



def Ordersarrived(request):
    if 'shop_email' not in request.session:
        messages.error(request, "You must be logged in as a shopkeeper.")
        return redirect('Shopkeeper')

    shop_email = request.session['shop_email']
    
    # Get the shopkeeper instance based on email
    shop = get_object_or_404(shopkeeper, email=shop_email)

    # Fetch orders where the product belongs to the shopkeeper's shop
    orders = buy.objects.filter(product__shop_id=shop.shop_id).order_by('-id')

    return render(request, 'ordersarrived.html', {'orders': orders})

def Yourorders(request):
    if 'user_email' not in request.session:
        messages.error(request, "You must be logged in to view orders.")
        return redirect('Signin')

    yemail = request.session['user_email']

    user = get_object_or_404(signup, email=yemail)

    yorders = buy.objects.filter(user=user).order_by('-id')

    return render(request, 'yourorders.html', {'yorders': yorders})


def ToggleShopStatus(request):
    if 'shop_email' not in request.session:
        messages.error(request, "Login as shopkeeper first")
        return redirect('Shopkeeper')

    shop = get_object_or_404(shopkeeper, email=request.session['shop_email'])

    # Toggle True ↔ False
    shop.is_open = not shop.is_open
    shop.save()

    return redirect('Shopprofile')

def Toggleproductavailable(request):
    if 'shop_email' not in request.session:
        messages.error(request, "Login as shopkeeper first")
        return redirect('Shopkeeper')

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            messages.error(request, "Invalid product")
            return redirect("Shopprofile")

        product = get_object_or_404(addproduct, product_id=product_id)

        # 🔁 Toggle availability (same logic as shop open/close)
        product.is_avaiable = not product.is_avaiable
        product.save()

        messages.success(request, "Product availability updated")
        return redirect("Shopprofile")


def CancelOrderShop(request, id):
    if 'user_email' not in request.session:
        messages.error(request, "Login as shopkeeper first")
        return redirect('Shopkeeper')

    order = get_object_or_404(buy, id=id)

    order.delete()
    messages.success(request, "Order cancelled and removed.")

    return redirect('Customermain')


def OrderArrived(request, id):
    if 'user_email' not in request.session:
        messages.error(request, "Login as shopkeeper first")
        return redirect('Shopkeeper')

    order = get_object_or_404(buy, id=id)

    order.delete()
    messages.success(request, "Order marked as arrived and removed.")

    return redirect('Customermain')

def ConfirmOrder(request, id):
    if 'shop_email' not in request.session:
        messages.error(request, "Login as shopkeeper first")
        return redirect('Shopkeeper')

    order = get_object_or_404(buy, id=id)

    # Toggle confirmation
    order.is_confirmed = not order.is_confirmed
    order.save()

    if order.is_confirmed:
        messages.success(request, "Order confirmed successfully ✅")
    else:
        messages.info(request, "Order moved back to pending ⏳")

    return redirect('Ordersarrived')