from django.db import models
from store.models import Items
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, unique= True)
    date_added = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    Items = models.ForeignKey(Items,on_delete=models.CASCADE)  #Items is referring to the store Items
    User = models.ForeignKey(User,on_delete=models.CASCADE,null = True) #user is referring to the auth table user
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null = True) #cart refers to the class cart in the same carts app
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.Items.name
    
    def subtotal(self):
        return self.Items.price * self.quantity

