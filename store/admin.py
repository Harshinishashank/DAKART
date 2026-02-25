from django.contrib import admin
from .models import Items
# Register your models here.

#admin.site.register(Items)


#below code is to display the list of items in the db
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name','price','created_at','updated_at','description')

admin.site.register(Items,ItemsAdmin)