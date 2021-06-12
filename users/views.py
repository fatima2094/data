from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import View, FormView

from django.contrib.auth.models import User

from  django.contrib.auth.views   import LoginView
from django.contrib import messages
from .forms import SignUpForm,LoginForm
from .models import code
from . import forms
from cryptography.fernet import Fernet

from django.conf import settings


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()





write_key()
key = load_key()
ckey = key.decode()
####################################################################
class SignUpView(FormView):
    template_name = 'app/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        Email =  user.email

        # Create a user record
       
        user.first_name=ckey
        ds = user.first_name
        print('last',ds)
        

        # Change the username to the "user_ID" form
        
       
        #raw_password = form.cleaned_data['password1']
        password = form.cleaned_data.get('password1')
        user.is_active = False
        
        user.save()
        #user = authenticate(username=user.username, password=password)
        
        login(request, user)
        sec = emailmsg("Encryption Key"," Key is: "+ckey,Email)

        messages.success(request, ("You are successfully signed up! \n You must wait for the official's approval"))

        return redirect('login')


#########################################################

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			lastname = form.cleaned_data.get('lastname')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			""" form.username = ckey
			ds =form.username
			print ("lastname   Last name:",ds) """
			form.save()
			login(request, user)
			
			sec = emailmsg("Encryption Key"," Key is: "+ckey,email)
			return redirect('login')
		else:
			messages.error(request, 'Correct the errors below')
	else:
		form = SignUpForm()

	return render(request, 'app/signup.html', {'form': form})


@login_required
def dashboard_view(request):
	return render(request, 'app/dashboard.html')


def home_view(request):
	return render(request, 'app/home.html')



#####

import smtplib
from email.message import EmailMessage
import random
import os
from .models import code


EOTP = random.randint(10000,99999) #Generate a five digit random number.


def emailmsg(subject, body,to):
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to
	user = "fatimhalbshir@gmail.com"
	msg['from'] = user

	password = "ptqeqsynwoqipbgl"

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(user,password)
	server.send_message(msg)
	server.quit()


class LoginUser(LoginView):
    template_name = 'registration/login.html'  # your template
    from_class = forms.LoginForm  # your form
    
   

class add_Code_view(View):
	template_name = 'registration/otp.html' 
	#code = code.objects.get(otp=otp)


def	auth(request):
	Email = None
	x = request.user.email
	#print("cccc",x)
	qrcode = emailmsg("authentcations"," Your OTP Code is: "+str(EOTP),x)
	print(EOTP)
	if request.method == "POST":
		otp = request.POST['otp']
		Email = request.user.email
		#print(str(Email)+"kkk%s"%EOTP) 
		if otp == str(EOTP):
			

			return redirect("file_upload:file_list")
		else:
		    messages.warning(request, "Error you Enter Wrong CODE")
            #return redirect("login")
	

	return render(request,'registration/otp.html' )



