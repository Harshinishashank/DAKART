from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address_line1 = models.TextField(max_length=250)
    address_line2 = models.TextField(max_length=250)
    profile_picture = models.ImageField(upload_to='profile_pics/',null = True,blank = True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    Phone_no = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username