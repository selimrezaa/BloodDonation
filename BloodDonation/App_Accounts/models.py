from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICE=(
    ('male','Male'),
    ('female','Female'),
)
SELECT_BLOOD_GROUP=(
    ('A+','A+'),
    ('B+','B+'),
    ('O+','O+'),
    ('AB+','AB+'),
    ('A-','A-'),
    ('B-','B-'),
    ('O-','O-'),
    ('AB-','AB-'),
)
USER_TYPE=(
    ('permanent','Permanent'),
    ('blood doner','Blood Doner'),
    ('money doner','MOney Doner'),
)

RELIGION_CHOICE=(
    ('muslim','Muslim'),
    ('hinduism','Hinduism'),
    ('buddhism','Buddhism'),
    ('christianity','Christianity'),
)
class BloodGroup(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    type=models.CharField(choices=USER_TYPE,max_length=20,blank=True)
    phone=models.CharField(blank=True,max_length=11)
    city=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=100)
    facebook=models.CharField(blank=True,max_length=100)
    twitter=models.CharField(blank=True,max_length=100)
    instragam=models.CharField(blank=True,max_length=100)
    linkedin=models.CharField(blank=True,max_length=100)
    gender=models.CharField(choices=GENDER_CHOICE,blank=True,max_length=30)
    bloodgroup=models.CharField(choices=SELECT_BLOOD_GROUP,blank=True,null=True,max_length=20)
    religion=models.CharField(blank=True,max_length=20,choices=RELIGION_CHOICE)
    totaldonate=models.IntegerField(default=0)
    image=models.ImageField(upload_to="Profile",default="avatar7.png")
    dob=models.DateField(blank=True,null=True)
    lastdonate=models.DateField(blank=True,null=True)
    aboutyou=models.TextField(blank=True)

    def __str__(self):
        return '{}-{}'.format(self.user,self.type)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
