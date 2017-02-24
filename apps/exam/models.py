from __future__ import unicode_literals
import bcrypt, re
from django.db import models
import datetime
# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        error_msgs = []
        password = bcrypt.hashpw(postData['pass'].encode(), bcrypt.gensalt())

        try:
            user = User.objects.get(email=postData['email'])
        except:
            error_msgs.append("Invalid user!")
            return {'errors':error_msgs}

        if not bcrypt.hashpw(postData['pass'].encode(), user.password.encode()) == user.password.encode():
            error_msgs.append("Wrong Password!")

        if error_msgs:
            return {'errors':error_msgs}
        else:
            return {'theuser':user.name, 'userid':user.id}

    def register(self, postData):
        error_msgs = []
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        try:
            if User.objects.get(email=postData['email']):
                error_msgs.append("Email already in use!")
        except:
            pass

        if len(postData['name']) < 2:
            error_msgs.append("Name is too short!")

        if not email_regex.match(postData['email']):
            error_msgs.append("Invalid email!")

        if len(postData['pass']) < 8:
            error_msgs.append("Password is too short!")

        if not postData['pass'] == postData['pass_conf']:
            error_msgs.append("Passwords do not match!")

        if error_msgs:
            return {'errors':error_msgs}
        else:
            hashed = bcrypt.hashpw(postData['pass'].encode(), bcrypt.gensalt())
            user = User.objects.create(email=postData['email'],name=postData['name'], password=hashed)
            return {'theuser':user.name, 'userid': user.id}

class User(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class TravelManager(models.Manager):
    def add(self, postData, userid):
        error_msgs = []
        if len(postData['destination']) < 1:
            error_msgs.append('Destination name required')

        if len(postData['plan']) < 1:
            error_msgs.append('Travel plans required')

        today = datetime.datetime.today()
        start = datetime.datetime.strptime(postData['startdate'], '%Y-%m-%d')
        ##figure out how to convert inputs to unicode to compare
        if start < today:
            error_msgs.append('Must pick a future date')
        #

        if postData['enddate'] < postData['startdate']:
            error_msgs.append('Must return after you leave.')

        user = {'user': User.objects.get(id=userid)}
        if error_msgs:
            return {'errors':error_msgs}
        else:
            travel = Travel.objects.create(destination=postData['destination'], startdate=postData['startdate'], enddate=postData['enddate'], plan=postData['plan'], user=user['user'])
            return {'destination' :travel.destination}

    def join(self, postData, userid):
        travel = Travel.objects.get(id=postData)
        travel = Travel.objects.create(destination=postData['destination'], startdate=postData['startdate'], enddate=postData['enddate'], plan=postData['plan'], user=userid)
        return

class Travel(models.Model):
    destination = models.CharField(max_length=75)
    startdate = models.DateField()
    enddate = models.DateField()
    plan = models.TextField()
    user = models.ForeignKey(User, related_name="travel")
    objects = TravelManager()
