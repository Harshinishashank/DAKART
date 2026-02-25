from django.db import models

# Create your models here.
class Category(models.Model):
    category_name= models.CharField(max_length=100)
    slug = models.SlugField(max_length=10, unique=True)
    description = models.TextField(blank=True,null=True)



    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
