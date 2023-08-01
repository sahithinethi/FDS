from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.contrib.auth.forms import PasswordChangeForm
STATE_CHOICES =(("Andaman & Nicobar Islands","Andaman & Nicobar Islands"),
                ("Andhra Pradesh","Andhra Pradesh"),
                ("Arunachal Pradesh","Arunachal Pradesh"),
                ("Assam","Assam"),
                ("Bihar","Bihar"),
                ("Chandigarh","Chandigarh"),
                ("Chattisgarh","Chattisgarh"),
                ("Dadra & Nagar Haveli","Dadra & Nagar Haveli"),
                ("Daman & Diu","Daman & Diu"),
                ("Delhi","Delhi"),
                ("Goa","Goa"),
                ("Gujarat","Gujarat"),
                ("Haryana","Haryana"),
                ("Himachal Pradesh","Himachal Pradesh"),
                ("Jammu & Kashmir","Jammu & Kashmir"),
                ("Jharkhand","Jharkhand"),
                ("Karnataka","Karnataka"),
                ("Kerala","Kerala"),
                ("Lakshadweep","Lakshadweep"),
                ("Madhya Pradesh","Madhya Pradesh"),
                ("Maharashtra","Maharashtra"),
                ("Manipur","Manipur"),
                ("Meghalaya","Meghalaya"),
                ("Mizoram","Mizoram"),
                ("Nagaland","Nagaland"),
                ("Odisha","Odisha"),
                ("Puducherry","Puducherry"),
                ("Punjab","Punjab"),
                ("Rajasthan","Rajasthan"),
                ("Sikkim","Sikkim"),
                ("Tamil Nadu","Tamil Nadu"),
                ("Telangana","Telangana"),
                ("Tripura","Tripura"),
                ("Uttarakhand","Uttarakhand"),
                ("Uttar Pradesh","Uttar Pradesh"),
                ("West Bengal","West Bengal"),
                )

#customer model
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=50)
    def __str__(self) -> str:
        return str(self.id)

CATEGORY_CHOICES=(
    ('MT','MEN-TOPWEAR'),
    ('MB','MEN-BOTTOMWEAR'),
    ('WI','WOMEN-INDIAN'),
    ('WW','WOMEN-WESTERN'),
    ('MA','MEN-ACC'),
    ('WA','WOMEN-ACC'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    colour =models.CharField(max_length=100,default=' ')
    fabric = models.CharField(max_length=100,default=' ')
    sizes = models.CharField(max_length=100,default=' ')
    feedback = models.CharField(max_length=100,default=' ')
    def __str__(self) -> str:
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel'),  
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class CustomerRequest(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    req = models.CharField(max_length=1000,default=' ')
    status=models.CharField(max_length=1000,default='passed to the designer')
    
    def __str__(self) -> str:
        return str(self.id)
