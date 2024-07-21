from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from . models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, BuyNow
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.conf import settings


# Create your views here.
def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',locals())

def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())

def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.get(pk=pk)
        wishlist= Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        return render(request,'app/productdetail.html',locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! User Registration Successful')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request, 'app/customerregistration.html',locals())
    


class ProfileView(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality'] 
            mobile=form.cleaned_data['mobile']
            city=form.cleaned_data['city']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data") 
        return render(request,'app/profile.html',locals())


def address(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality'] 
            add.mobile = form.cleaned_data['mobile']
            add.city = form.cleaned_data['city']
            add.zipcode = form.cleaned_data['zipcode'] 
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning (request, "Invalid Input Data")
        return redirect("address")
    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def buy_now(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    BuyNow(user=user, product=product).save()
    return redirect("/buynow")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value= p.quantity * p.product.discounted_price
        amount=amount+value
    totalamount= amount+40
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

def show_buynow(request):
    user=request.user
    buynow=BuyNow.objects.filter(user=user)
    amount=0
    for p in buynow:
        value= p.quantity * p.product.discounted_price
        amount=amount+value
    totalamount= amount+40
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/buynow.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40
        data={
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value= p.quantity * p.product.discounted_price
            famount=famount+value
        totalamount= famount+40
        razoramount= int(totalamount * 100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data={"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response=client.order.create(data=data)
        print(payment_response)
#{'id': 'order_MHeOiILsJwdIzN', 'entity': 'order', 'amount': 14150, 'amount_paid': 0, 'amount_due': 14150, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1690204354}
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())
    

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id') 
    cust_id=request.GET.get('cust_id')
    #print("payment_done : oid = ",order_id," pid = ",payment_id," cid = ",cust_id) 
    user=request.user
#return redirect("orders")
    customer=Customer.objects.get(id=request.GET.get('cust_id'))
#To update payment status and payment id 
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
#To save order details
    carts=Cart.objects.filter(user=user)
    for c in carts:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save() 
        c.delete()
    return redirect("orders")

def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id'] 
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id'] 
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={  
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    
def remove_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c= Wishlist.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
        amount=0
        data={
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    
def add_to_wishlist(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Wishlist(user=user, product=product).save()
    return redirect("/wishlist")

def show_wishlist(request):
    user=request.user
    wishlist=Wishlist.objects.filter(user=user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtowishlist.html',locals())

def search(request):
    query=request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())
