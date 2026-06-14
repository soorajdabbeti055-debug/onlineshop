from django.shortcuts import render, redirect, get_object_or_404
from .models import shopkeeper,addproduct,signup,buy
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

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
            shop = shopkeeper.objects.filter(district=user.district,mandal=user.mandal)
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
            password=password  # Will be hashed in `save()`
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
        exists_user=signup.objects.filter(email=email).exists()
        if exists_user:
            messages.error(request, 'User already exists!')
            return redirect('Signup')
        else:
            user=signup(username=username,email=email,password=password,district=district,mandal=mandal,village=village,area=area)
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
        shop = shopkeeper.objects.filter(district=user.district,mandal=user.mandal)
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

def Buy(request, id):
    if 'user_email' not in request.session:
        messages.error(request, "You must be logged in to buy a product.")
        return redirect('Signin')

    product = get_object_or_404(addproduct, product_id=id)  # ✅ Ensure correct product ID
    user_email = request.session['user_email']
    user = get_object_or_404(signup, email=user_email)  # ✅ Fetch user

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            number = request.POST.get('number')

            if quantity <= 0:
                messages.error(request, "Invalid quantity.")
                return redirect('Shopproductdetails', id=id)

            new_purchase = buy(
                product=product,  # ✅ Save the product instance
                product_image=product.productimageone,  # ✅ Save the image separately
                user=user,
                quantity=quantity,
                number=number
            )
            new_purchase.save()

            messages.success(request, f"Successfully bought {quantity} {product.productname}(s).")
            return redirect('Customermain')

        except ValueError:
            messages.error(request, "Invalid quantity input.")
            return redirect('Shopproductdetails', id=id)

    return render(request, 'buy.html', {'product': product})

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
