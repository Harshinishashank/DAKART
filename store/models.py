from django.db import models
from category.models import Category

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length= 100)
    slug = models.SlugField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/items/')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    category_table = models.ForeignKey(Category,on_delete= models.CASCADE, default = 1)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


    def __str__(self):
        return self.name
    
    