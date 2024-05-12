from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Vendors(AbstractUser):
    username = models.CharField(max_length= 100,blank=True,null= True)
    contact_details = models.TextField(blank=True,null= True)
    address = models.TextField(blank=True,null= True)
    vendor_code = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length= 100)
    on_time_delivery_rate = models.FloatField(blank=True,null=True)
    quality_rating_avg = models.FloatField(blank=True,null=True)
    average_response_time = models.FloatField(blank=True,null=True)
    fulfillment_rate = models.FloatField(blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'vendor_code'

    def __str__(self):
        return str(self.id)
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
    


order_choice=(
    ('pending','pending'),
    ('completed','completed'),
    ('canceled','canceled')
)
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50,unique=True)
    vendor = models.ForeignKey( Vendors,on_delete = models.CASCADE )
    order_date = models.DateTimeField(auto_now_add = True)
    delivery_date = models.DateTimeField(blank= True,null=True)
    items = models.JSONField(blank= True,null=True)
    quantity = models.IntegerField(blank= True,null=True)
    status = models.CharField(max_length=50,choices = order_choice,blank= True,null=True)
    quality_rating = models.FloatField(blank= True,null=True)
    issue_date = models.DateTimeField(blank= True,null=True)
    acknowledgment_date = models.DateTimeField(blank= True,null=True)

    def __str__(self):
        return str(self.id)



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendors,on_delete= models.CASCADE)
    date = models.DateTimeField(blank= True,null=True)
    on_time_delivery_rate = models.FloatField(blank=True,null=True)
    quality_rating_avg = models.FloatField(blank=True,null=True)
    average_response_time = models.FloatField(blank=True,null=True)
    fulfillment_rate = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.id)