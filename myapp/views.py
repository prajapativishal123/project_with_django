from django.shortcuts import render
from .models import User
import requests
import random
# Create your views here.
def index(request):
    return render(request,'index.html') 

def category(request):
    return render(request,'category.html')

def single_product(request):
    return render(request,'single-product.html')

def checkout(request):
    return render(request,'checkout.html')

def cart(request):
    return render(request,'cart.html')

def blog(request):
    return render(request,'blog.html')

def single_blog(request):
    return render(request,'single-blog.html')

def tracking(request):
    return render(request,'tracking.html')

def elements(request):
    return render(request,'elements.html')

def contact(request):
    return render(request,'contact.html') 

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        password=request.POST['password'],
                        profile_picture=request.FILES.get('profile_picture')
                    )
                msg="User Registered Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'signup.html',{'msg':msg})
    
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                request.session['profile_picture']=user.profile_picture.url
                return render(request,'index.html')
            else:
                msg="Incorrect Password" 
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registered"
            return render(request,'login.html',{'msg':msg})           
    else:
        return render(request,'login.html') 

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
        msg="User Logged Out Successfully"
        return render(request,'login.html',{'msg':msg}) 
    except:
        msg="User Logged Out Successfully"
        return render(request,'login.html',{'msg':msg})                  

def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        msg="profile Updated Successfully" 
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:        
        return render(request,'profile.html',{'user':user})

def change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    msg="Password Changed Successfully. Please Login Again."
                    del request.session['email']
                    del request.session['fname']
                    del request.session['profile_picture']
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg="Your New Password Can't Be From Your Old Password"
                    return render(request,'change-password.html',{'msg':msg})
            else:
                msg="New Password & Confirm New Password Does Not Matched"
                return render(request,'change-password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'change-password.html',{'msg':msg})               
    else:    
        return render(request,'change-password.html')

def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(mobile=request.POST['mobile'])
            otp=str(random.randint(9997,9999))
            mobile=str(request.POST['mobile'])
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
                "authorization": "GNEfP9pvQ4DjK6wkMrxiqL3tYhgcoUSF0RdObInAHe852Bms17xoVJc6tRKA8iXu0bfejvDkynaGLqNz",
                "variables_values": otp,  # Pass the actual OTP value
                "route": "otp",
                "numbers": mobile
            }
            headers = {'cache-control': "no-cache"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            request.session['otp']=otp
            request.session['mobile']=mobile
            msg="OTP Send Successfully"
            return render(request,'otp.html',{'msg':msg})
        except:
            msg="Mobile Not Registered"
            return render(request,'forgot-password.html',{'msg':msg})    
    else:    
        return render(request,'forgot-password.html')

def verify_otp(request):
    otp1=int(request.session['otp'])
    otp2=int(request.POST['otp'])

    if otp1==otp2:
        msg="Set Your New Password" 
        del request.session['otp']
        return render(request,'new-password.html',{'msg':msg}) 
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'msg':msg}) 

def new_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(mobile=request.session['mobile'])
        user.password=request.POST['new_password']  
        user.save()
        del request.session['mobile']
        msg="Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New Password & Confirm New Password Does Not Matched"
        return render(request,'new-password.html',{'msg':msg})   