
from django.views import View 
from django.contrib.auth.views import PasswordChangeView
from .models import Customer,Product,Cart,OrderPlaced
from .models import *
from django.urls import reverse_lazy
from .forms import CustomerRegistrationForm,CustomerProfileForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail,EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import *
from django.template import loader
from django.contrib.auth.forms import PasswordChangeForm
from .forms import MyPasswordChangeForm
from django.shortcuts import render,redirect

from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
     
class ProductView(View):
    def  get(self,request):
        
        topwears = Product.objects.filter(category='MT')
        bottomwears = Product.objects.filter(category='MB')

        indianwears =Product.objects.filter(category='WI')

        westernwears=Product.objects.filter(category='WW')
        return render(request,'app/home.html',{'topwear':topwears,'bottomwear':bottomwears,'indianwear':indianwears,'westernwear':westernwears})



# def home(request):
#  return render(request, 'app/home.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk=None):
        product =Product.objects.get(pk=pk)
        item_already_in_cart =False
        item_already_in_cart =Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists
        return render(request,'app/productdetail1.html',{'product':product,'item_already_in_cart':item_already_in_cart})

# @login_required
def add_to_cart(request):
    user=request.user
    product_id= request.GET.get('prod_id')
    product =Product.objects.get(id=product_id)
    print(product_id)
    Cart(user=user,product=product).save()
    
    
    return redirect('/cart')

def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#     return render(request, 'app/profile.html')
# @login_required
def address(request):
    add =Customer.objects.filter(user=request.user)
    
    return render(request, 'app/address.html',{'add':add,"active":"btn-primary"})
# @login_required
def orders(request):
    user=request.user
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
    return render(request, 'app/changepassword.html')

def men_top(request,data=None):
    if data == None:
        mt = Product.objects.filter(category='MT')
    else:
        mt = Product.objects.filter(category='MT').filter(brand=data)
    return render(request, 'app/men_top.html',{'mt':mt})

def women_acc(request):
    mt = Product.objects.filter(category='WA')
    return render(request,'app/womenacc.html',{'wa':mt})

def men_acc(request):
    mt = Product.objects.filter(category='MA')
    return render(request,'app/menacc.html',{'ma':mt})
    



def men_bottom(request,data=None):
    if data == None:
        mb = Product.objects.filter(category='MB')
    else:
        mb = Product.objects.filter(category='MB').filter(brand=data)
    return render(request, 'app/men_bottom.html',{'mb':mb})

def women_indian(request,data=None):
    if data == None:
        wi = Product.objects.filter(category='WI')
    else:
        wi = Product.objects.filter(category='WI').filter(brand=data)
    return render(request, 'app/women_indian.html',{'wi':wi})



def women_western(request,data=None):
    if data == None:
        ww = Product.objects.filter(category='WW')
    else:
        ww = Product.objects.filter(category='WW').filter(brand=data)
    return render(request, 'app/women_western.html',{'ww':ww})


def signin(request):
    # lg = login.objects.all().values()
    if request.method == 'POST':
        username = request.POST.get('uname')
        pass1 = request.POST.get('password')
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            a=username
            print(a)
            return render(request, 'app/home.html')
        else:
            messages.error(request, "wrong credentials")
            a=None
            print(a)
            return redirect('home')
    return render(request, "app/login.html", {})

# def customerregistration(request):
#     return render(request, 'app/
#     customerregistration.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        # phno=request.POST.get('Phnum')
        email = request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists please try some other username')
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, 'Email exists please try some other username')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "password did'nt match")
        
        print(username,fname,lname,email,pass1,pass2)
        myuser =User.objects.create_user(username,email,pass1)

        myuser.first_name=fname
        myuser.last_name=lname
        # myuser.contact_number=phno
        myuser.is_active=False
        myuser.save()
        messages.success(request,
                         'your account has beem sucessfully created we have sent you a confirmation email please confirm your email to activate your account')
        
        # welcome email
        subject = "welcome to fds -django login"
        message = "hello" + myuser.first_name + "!! \n" + "welcome to FDS\nThanku for visiting our website we have " \
                                                          "also sent you a confirm email address in order to activate " \
                                                          "your account.\n\n Thanking You\n JAYA RAM SAMAVEDAM " \
                                                          "\ncontact number:99479837192\n organisation-name:IMASH\n " \
                                                          "FOUNDER,CEO "

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list)
        # verification email
        current_site = get_current_site(request)
        email_subject = "confirm your email @fds -DJango login!!"
        message2 = render_to_string('app/email_confirmation.html',
                                    {'name': myuser.first_name, 'domain': current_site.domain,
                                     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                                     'token': generate_token.make_token(myuser)})
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        a=username
        return redirect('login')

    return render(request, "app/register.html", {})


def activate(request,uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        myuser =User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'app/activation_failed.html')

            
def signout(request):
    logout(request)
    messages.success(request, "logged out sucessfully")
    a=None
    return redirect('home')        


@method_decorator(login_required,name='dispatch')
class ProfileView(View)  :
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulations profile updated sucessfully")
            return render(request,'app/profile.html',{'form':form,"active":"btn-primary"})



# @login_required
def show_cart(request):
    if request.user.is_authenticated:
        request.session['forward']=True
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount = 70.0
        total_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
            total_amount=amount+shipping_amount
            print(cart)
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        #id from ajax == cart users product id 
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount = 70.0
        total_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
                total_amount=amount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount+shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        #id from ajax == cart users product id 
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount = 70.0
        total_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
                total_amount=amount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount+shipping_amount
        }
        return JsonResponse(data)

# @login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        #id from ajax == cart users product id 
        c.delete()
        amount=0.0
        shipping_amount = 70.0
        total_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
                total_amount=amount
        data={
            
            'amount':amount,
            'totalamount':total_amount+shipping_amount
        }
        return JsonResponse(data)



def checkout(request):
    
    request.session['p'] = True
    user =request.user
    add=Customer.objects.filter(user=user)
    cart_items= Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount = 70.0
    total_amount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
    print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+=tempamount
        total_amount=amount+shipping_amount
    if not request.session['p']:
        return redirect('home')
    else:
        return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_items':cart_items})


# @login_required
def payment_done(request):
    
    user=request.user
    custid =request.GET.get('custid')
    customer =Customer.objects.get(id=custid)
    cart =Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    request.session['p']=False   
    return redirect("orders")
def raiserequest(request):
    
    return render(request,'app/raiserequest.html',{})



def  PasswordsChangeView(PasswordChangeView):
    from_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_sucess')
    
    
    # sucess_url =reverse_lazy('password_sucess')


def password_sucess(request):
    return render(request,'app/password_sucess.html')