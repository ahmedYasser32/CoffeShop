import math
import os
import random
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


#A class to Manage users and create users in django
class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#Customer class that overrides the django built in abstract base user
class Customer(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= None
    firstname               = models.CharField(max_length=25,null = False,default="firstname")
    lastname                = models.CharField(max_length=25,null = False,default="lastname")
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    verified                = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email


def image_upload_path(instance, filename):
    upload_to = 'media/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        filename = '{}.{}'.format(instance.name, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Category(models.Model):
    name          = models.CharField(max_length=200)



class Item(models.Model):

  name          = models.CharField(max_length=200)
  description   = models.CharField(max_length=500)
  created_at	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
  modified_at   = models.DateTimeField(verbose_name='date modified',null=True)
  price         = models.IntegerField( null=False)
  isavaliable   = models.BooleanField(default=True)
  isdiscount    = models.BooleanField(default=False)
  discount      = models.IntegerField(default=0, null=True, blank=True)
  picture       = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
  category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)



class Address(models.Model):

    customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address    = models.CharField(max_length=200, null=False)
    street     = models.CharField(max_length=200, null=False)
    bulding    = models.CharField(max_length=200, null=False)
    postalcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address


class Order(models.Model):

     statuses       = [(1,"preparing"),(2,"Ready"),(3,"Delivering"),(4,"Delivered"),(-1,"Cancelled"),(0,"Pending")]
     created_at	    = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
     status         = models.SmallIntegerField(choices=statuses,default=0)
     total_price    = models.PositiveIntegerField(default=0)
     isdiscount     = models.BooleanField(default=False)
     discount       = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)],default=0)
     customer       = models.ForeignKey(Customer, on_delete=models.CASCADE)
     iscomplete     = models.BooleanField(default=False)
     transaction_id = models.CharField(max_length=10, null=True)
     promocode      = models.CharField(max_length=10, null=True)



     @property
     def get_cart_total(self):
         orderitems = self.orderitem_set.all()
         total = sum([item.get_total for item in orderitems])
         return total



     @property
     def get_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):

    item       = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order      = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity   = models.IntegerField(default=0, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price      = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total


