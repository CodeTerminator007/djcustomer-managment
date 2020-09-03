from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    USERNAME_FIELD = 'name'
    user = models.OneToOneField(User , null=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200 , null=True)
    phone = models.CharField(max_length=200 , null=True)
    email = models.EmailField(max_length=200 , null=True)
    profile_pic = models.ImageField(null=True ,default='profile1.jpg', blank=True,)
    passwrod1 = models.CharField(max_length=20,default="adminadmin")
    date_created = models.DateTimeField(auto_now_add=True ,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200 , null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    CATAGORY = (
        ('Indoor', 'Idoor'),
        ('Outdoor', 'Outdoor'),

    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True) 
    Catagory = models.CharField(max_length=200,null=True , choices=CATAGORY)    
    description = models.CharField(max_length=200,null=True , blank=True) 
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending' , 'Pending'),
        ('Out of Deleviery' , 'Out of Deleviery'),
        ('Delivered' , 'Delivered'),
    )
    user = models.ForeignKey(User , null=True , on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer , null=True , on_delete=models.SET_NULL) 
    product = models.ForeignKey(Product,null=True , on_delete=models.SET_NULL) 
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)

    def __str__(self):
        return self.product

