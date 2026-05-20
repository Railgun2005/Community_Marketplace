from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    pfp = models.ImageField(upload_to='uploads/pfp/')
    theme = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Category(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'
    
class Item(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='uploads/item/')
    def __str__(self):
        return self.name
    
class Order(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    quantity = models.IntegerField()
    location = models.CharField(max_length=250,default='',blank=True)
    phone = models.CharField(max_length=20,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    order_type = models.BooleanField(default=False)
    def __str__(self):
        return self.item.name
    def save(self, *args, **kwargs):
        if not self.location and hasattr(self.user, 'userprofile'):
            self.location = self.user.userprofile.address
        if not self.phone and hasattr(self.user, 'userprofile'):
            self.phone = self.user.userprofile.phone
        super().save(*args, **kwargs)