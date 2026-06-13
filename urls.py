from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shopapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Allhome, name='Allhome'),
    path('shopkeeper/', views.Shopkeeper, name='Shopkeeper'),
    path('shopkeeper/reopenshop/', views.Reopenshop, name='reopenshop'),  # Fixed name
    path('customer/', views.Customer, name='Customer'),
    path('shopprofile/', views.Shopprofile, name='Shopprofile'),
    path('productdetails/<int:id>/',views.Productdetails, name='Productdetails'),
    path('leaveshop/', views.Leaveshop, name='Leaveshop'),
    path('shopprofile/leaveshop',views.Leaveshop, name='Leaveshop'),
    path('addproduct/', views.Addproduct, name='Addproduct'),
    path('signup/',views.Signup, name='Signup'),
    path('signout/', views.Signout, name='Signout'),
    path('signup/signin/',views.Signin,name='Signup'),
    path('customermain/',views.Customermain, name='Customermain'),
    path('customermain/signout/',views.Signout,name='Signout'),
    path('shopproduct/<int:id>/',views.Shopproduct, name='Shopproduct'),
    path('shopproductdetails/<int:id>/',views.Shopproductdetails, name='Shopproductdetails'),
    path('shopproductdetails/<int:id>/buy/',views.Buy,name='Buy'),
    path('ordersarrived/',views.Ordersarrived,name='Ordersarrived'),
    path('yourorders/',views.Yourorders,name='Yourorders'),
    path('toggle-shop/', views.ToggleShopStatus, name='ToggleShopStatus'),
    path('ToggleProductStatus/',views.Toggleproductavailable,name='ToggleProductStatus'),
    path('signup/signin/', views.Signin, name='signin'),
    path('yourorders/', views.Yourorders, name='Yourorders'),
    path('cancel-order-shop/<int:id>/', views.CancelOrderShop, name='CancelOrderShop'),
    path('order-arrived/<int:id>/', views.OrderArrived, name='OrderArrived'),
    path('verify-order-otp/', views.VerifyOrderOTP, name='VerifyOrderOTP'),
    path('confirm-order/<int:id>/', views.ConfirmOrder, name='ConfirmOrder'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#path('verify-order-otp/', views.VerifyOrderOTP, name='VerifyOrderOTP'),