from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
import smtplib
from email.message import EmailMessage

# Create your models here.


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

class code(models.Model):
    OTP = models.IntegerField(default=0, blank=False)

class UserProfile(models.Model):
  #address = models.CharField(max_length=300,blank=True,null=True,help_text=("enter the address"))
  contact = models.CharField(max_length=100,blank=True,null=True,help_text=("enter the contact"))
  user = models.ForeignKey(User ,on_delete=models.CASCADE)

  def __str__(self):
    return (self.user.username)

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

@receiver(post_save,sender=UserProfile)
def send_user_data_when_created_by_admin(sender, instance, **kwargs):

      first_name = instance.user.email
      print('first name is',first_name)
      last_name = instance.user.first_name
      #address = instance.address
      email = instance.user.email
      content = instance.contact
      html_content = "your first name:%s <br> last name:%s <br> address:%s"
      #message=EmailMessage(subject='welcome',body=html_content %(first_name,last_name,address),to=[email])

      #message.content_subtype='html'
      sec = emailmsg("Group secret Key"," Key is: "+content,email)


