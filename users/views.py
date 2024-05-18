from django.shortcuts import render
from users.models import UsersConfig
from django.http import HttpResponse;
from django.http import HttpResponseRedirect;
from django.contrib import messages
from twilio.rest import Client
import random
# from team.models import *

account_sid = 'ACd2a91ebb714d4eaba772ae08316898b2'
auth_token = '154c3447867c2cf18b3d5da0e2b68c58'

from django.http import HttpResponseRedirect
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

def home(request):
    return render(request, 'home.html')

def send_otp(request, to, otp, user_id):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_="+12562428967",
            body=f"Your OTP for exam portal verification is: {otp}. Please enter this code to proceed. Do not share this code with anyone for security reasons.",
            to="+91" + to,
        )
        print(message.sid)
        print("OTP sent successfully.")
        return HttpResponseRedirect(f"/otp/user/{user_id}")
    except TwilioRestException as e:
        messages.error(request,"Invalid Phone Number")
        return HttpResponseRedirect("/reg")
    except Exception as e:
        messages.error(request, "Invalid Phone Number")
        return HttpResponseRedirect("/reg")

def change_number(request):
	pass

def otp_verification_page(request,user_id):
    user_data = {"title": "Registration page", "user_id": user_id}
    return render(request, "otp_verification_page.html", user_data)


def otp_verify(request):
    if request.method == "POST":
        otp_value = request.POST.get("otp")
        user_id = request.POST.get("otp_user_id")

        try:
            user_config = UsersConfig.objects.get(id=user_id, otp=otp_value)
        except UsersConfig.DoesNotExist:
            messages.error(request, "OTP verification failed!")
            return HttpResponseRedirect(f"/otp/user/{user_id}")
        user_config.otp_verification = 1
        user_config.save()
        messages.success(request, "OTP Verify successfully.")
        return HttpResponseRedirect("/login")

def reg(request):
	title= {"title":"Registration page"}
	return render(request,"registration.html",title)
# Create your views here.
def regUser(request):
    for key, value in request.POST.items():
        if request.POST.get(key) == "":
            return render(request, "registration.html", {"error": True})

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        city = request.POST.get("city")
        state = request.POST.get("stateSelect")
        dataToregUser = UsersConfig.objects.filter(email=email).values()
        emailTouser = ""
        for data in dataToregUser:
            emailTouser = data["email"]
        # emailToregUser = UsersConfig.objects.values_list('email', flat=True).distinct()
        if emailTouser == "":
            if password == confirm_password:
                otp = random.randrange(1000, 9999)
                datauser = UsersConfig(
                    email=email,
                    password=password,
                    username=username,
                    phone=phone,
                    gender=gender,
                    state=state,
                    city=city,
                    otp=otp,
                )
                datauser.save()
                messages.success(request, "Account created! Welcome to our platform.")
                datauserid = datauser.id
                return send_otp(request,datauser.phone, datauser.otp, datauserid)
                #return HttpResponseRedirect("/login")
            else:
                messages.success(
                    request, "Confirm your password to proceed, for security purposes."
                )
                return HttpResponseRedirect("/reg")
        else:
            messages.success(request, "Account exists. Please log in to access.")
            return HttpResponseRedirect("/login")

def login(request):
	title= {"title":"Login page"}
	return render(request,"login.html",title)


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        dataToregUser = UsersConfig.objects.filter(email=email).values()
        emailTouser = ""
        for data in dataToregUser:
            emailTouser = data["email"]
        if emailTouser != "":
            emaild = dataToregUser[0]["email"]
            password = request.POST.get("password")
            passwordToregUser = dataToregUser[0]["password"]
            if dataToregUser[0]["otp_verification"] != 1:
                user_config = UsersConfig.objects.get(email=email)
                user_config.otp = random.randrange(1000, 9999)
                user_config.save()
                messages.error(request, "Verify OTP First!")
                return send_otp(request,user_config.phone, user_config.otp, user_config.id)
            if password == passwordToregUser:
                request.session["userid"] = dataToregUser[0]["id"]
                request.session["useremail"] = dataToregUser[0]["email"]
                if "url_key" not in request.session:
                    return HttpResponseRedirect("/exam-list")
                else:
                    return HttpResponseRedirect(request.session["url_key"])
            else:
                messages.error(
                    request, "Password error. Please re-enter and try again."
                )
                return HttpResponseRedirect("/login")
        else:
            messages.error(request, "No account found. Please create a new one.")
            return HttpResponseRedirect("/login")




def logout(request):
	request.session['userid'] = 0
	request.session['useremail'] = ""
	return HttpResponseRedirect('/login') 



def accessories(request):
	#categories = Category.objects.all()
	# prd=products.objects.all()
	categories = Category.objects.values('id','name')
	cat_product = []
	for cat in categories:
		prd=products.objects.filter(catid=cat['id'])
		categories=Category.objects.filter(id=cat['id'])
		#prdd=products.objects.filter(catid=cat['id']).values()
		if prd.exists():
			cat_product.append([categories,prd])
	print(cat_product);
	cart_product_form= CartAddProductForm()
    #data={'prd':prd,'cart_product_form':cart_product_form}
    #data={'prd':prd,'cart_product_form':cart_product_form,'categories':categories}
	return render(request,"accessories.html",{'cat_product':cat_product,'title':'Accessories'})

	#return render(request, 'accessories.html',{"title":"Accessories page",'categories':categories,'prd':prd})

def jeans(request):
	title = {'title':'jeans page'}
	return render(request, 'jeans.html',title)



def aboutus(request):
	title = {'title':'About Us'}
	return render(request, 'about_us.html',title)


def faq(request):
	title = {'title':'FAQs'}
	return render(request, 'faq.html',title)



def terms(request):
	title = {'title':'terms'}
	return render(request, 'terms.html',title)

def team(request):
	title = {'title':'team'}
	return render(request, 'team.html',title)

def custom_404_error(request, exception):
    return render(request, '404.html', status=404)