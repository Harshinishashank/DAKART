from django.shortcuts import render
from . forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from . models import UserProfile
from carts.models import CartItem
from DAKART.views import cart_id
from django.contrib import auth 
from django.core.mail import send_mail
from django.conf import settings    
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes   
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from carts.models import Cart

# Create your views here.
def Register(request):

    if request.method == 'POST':
        #when the user submits the registration form
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():   #reg_form.is_valid() checks all the validations mentioned in forms.py
            first_name = reg_form.cleaned_data['first_name']
            last_name = reg_form.cleaned_data['last_name']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            username = email.split('@')[0]  
            #check if user already exists , here iam checking with the email id
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:  #the firt_name, last_name, email, and password has to match with the db fields name
                print("USER DOES NOT EXIST, CREATING NEW USER")
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save()
                #mapping the user id with userfrofile table to know which user has which profile
                profile = UserProfile()
                profile.user_id = user.id
                profile.save()
                #SENDING EMAIL TO THE USER TO VERIFY THE ACCOUNT
                mail_subject = 'Please activate your account'
                current_site = get_current_site(request) #to get the url of the current site
                message = render_to_string('account_verification_email.html',{
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = [email,] #fetching the email from the form

                send_mail(mail_subject,message,settings.EMAIL_HOST_USER,to_email)
                print("VERIFICATION EMAIL SENT TO THE USER")
                return redirect('/accounts/login/?command=verification&email='+email)    #this line of code should only be used for the first time when the user registers

            else:
                messages.warning(request,'User with this email already exists')
                return render(request,'register.html')
               
        else:
            #if the form is not valid
            errors = reg_form.errors
            context = {'errors':errors}
            return render(request,'register.html',context)



    #when the user first visits the registration page or when the form is not valid
    form = RegistrationForm()
    context = {'form':form}

    return render (request,'register.html',context)


#when the user tries to login 
def login(request):
    cart_item = None
    if request.method == 'POST':
        entered_email = request.POST['username']
        entered_password = request.POST['password']
        loggedin_user = User.authenticate(username=entered_email,password=entered_password)
        #after login, checking to see if there are any items in the cart for that user using the session key, because once you login the session key is deleted
        if loggedin_user is not None:
            #here we are checking if there is any cart items using the session key which is in Cart function
            try:
                cart_item = Cart.objects.get(cart__cart_id = cart_id(request))
            except cart_item.DoesNotExist:
                cart_item = None
            #if there are any cart items exists for that session key then we are going to assign those cart items to the logged in user
            #   
            is_cart_item_exists = CartItem.objects.filter(cart = cart_item).exists()

            if is_cart_item_exists:
                cart_items = CartItem.objects.filter(cart = cart_item)
                #updating the user id in the cart item table and assigning the cart items to the logged in user
                for item in cart_items:
                    item.User = loggedin_user
                    item.save() 
            auth.login(request,loggedin_user)
            return redirect('mainpage')    
            
        #if the login functionality fails    
        else:
            messages.error(request,'Invalid login credentials') 
            return redirect('login')        


       
    return render(request,'login.html')

def activate(request, uid64 , token):
    try: 
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.warning(request,"Invalid activation link")
        return redirect('register')

def dashboard(request):
    return render(request,'dashboard.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'You have logged out')
    return redirect('login')