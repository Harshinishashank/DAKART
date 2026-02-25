"""
URL configuration for DAKART project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from Accounts import views as Accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loadmainpage, name = "main_page"),
    path('store/', views.store, name = "store"),
    path('category/<slug:category_slug>', views.store, name = "category_name"),
    path('product_detail/<slug:category_slug>/<slug:product_slug>',views.product_detail,name = "product_detail"),
    path('add_cart/<int:proid>', views.addcart, name = "add_cart"),
    path('remove_cart_item/<int:proid>', views.removecart_item, name = "remove_cart_item"),
    path('increment_cart_Item/<int:proid>', views.increment_cartItem, name = "increment_cart_Item"),
    path('decrement_cart_Item/<int:proid>', views.decrement_cartItem, name = "decrement_cart_Item"),
    path('login/', Accounts_views.login, name="login"),
    path('logout/', Accounts_views.logout, name="logout"),
    path('activate/<uid64>/<token>', Accounts_views.activate, name="user_activate"),
    path('dashboard/', Accounts_views.dashboard, name="dashboard"),
    path('cart/',views.cart,name = "cart"),
    path('Register/',Accounts_views.Register,name = 'register'),
    path('checkout/', views.checkout, name="checkout"),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)