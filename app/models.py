from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="profiles",blank=True,null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10)
    city=models.CharField(max_length=30)
    address=models.TextField()
    wallet=models.FloatField(default=0)
    def __str__(self):
        return self.user.username
class Category(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='categories')
    def __str__(self):
        return self.name
class Slider(models.Model):
    image=models.ImageField(upload_to="slider")
    redirect_url=models.URLField()
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='posts')
    gender=models.CharField(max_length=20,default="All Genders",choices=(("All Genders","All Genders"),("Men","Men"),("Women","Women")))
    description = models.TextField()
    quantity=models.IntegerField(default=1)
    price = models.FloatField()
    rent_method=models.CharField(max_length=10,choices=(("1","Day"),("7","Week"),("30","Month"),("365","Year")))
    availability=models.BooleanField(default=True)
    location=models.CharField(max_length=20)
    period=models.DateField(default=datetime.date.today()+datetime.timedelta(days=365))
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class PostImage(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="posts")
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)  
    subject=models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    comment=models.TextField()
    empty=models.CharField(max_length=10,blank=True,null=True)
    image=models.ImageField(upload_to='comments',null=True,blank=True)
    rating=models.CharField(choices=(("1","1"),("12","2"),("123","3"),("1234","4"),("12345","5")),max_length=5)
class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_received')  
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_given')  
    subject=models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    comment=models.TextField()
    empty=models.CharField(max_length=10,blank=True,null=True)
    image=models.ImageField(upload_to='comments',null=True,blank=True)
    rating=models.CharField(choices=(("1","1"),("12","2"),("123","3"),("1234","4"),("12345","5")),max_length=5)
class Order(models.Model):
    payment_id=models.CharField(max_length=100,blank=True)
    order_id=models.CharField(max_length=100)
    ecommerce_id=models.CharField(max_length=100)
    payment_status=models.BooleanField(default=False)
    delivery_status=models.CharField(max_length=20,choices=(("Confirmed","Confirmed"),("Cancelled","Cancelled"),("Shipping","Shipping"),("Shipped","Shipped"),("Out for Delivery","Out for Delivery"),("Delivered","Delivered"),("Returned","Returned"),("Refunded","Refunded"),("Refund Cancel","Refund Cancel")))
    order_status=models.BooleanField(blank=True,default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Post,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    subtotal=models.DecimalField(max_digits=10,decimal_places=2)
    delivery_type=models.CharField(default="Courier",max_length=20,choices=(("Courier","Courier"),("Self Pickup","Self Pickup")))
    shipping=models.IntegerField(default=50)
    platform_fee=models.IntegerField(blank=True,null=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    full_name=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=10)
    alternate_no=models.CharField(max_length=10)
    address=models.TextField()
    pin_code=models.CharField(max_length=6)
    order_date=models.DateField(null=True,blank=True)
    delivery_date=models.DateField(null=True,blank=True)
    rent_start=models.DateField()
    rent_end=models.DateField()
    qrcode=models.ImageField(null=True,blank=True,upload_to='qrcodes')