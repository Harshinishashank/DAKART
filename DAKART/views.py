from django.shortcuts import render, redirect
from store.models import Items
from category.models import Category
from django.shortcuts import get_object_or_404
from carts.models import Cart
from carts.models import CartItem
from store.models import Items



def loadmainpage(request):
    items = Items.objects.all()
    context = {'items' : items}
    return render(request,'products.html',context) #call the products.html file, include the base.html in products.html 


def store(request, category_slug  = None):
    print("category_slug: ", category_slug)
    if category_slug != None:
        categories = get_object_or_404 (Category,slug = category_slug)
        store_data = Items.objects.filter(category_table = categories)
    else:
        store_data = Items.objects.all()

    store_count = store_data.count()

    print("STORE ITEMS:", store_data)
    context = {'item_store' : store_data, 'store_count':store_count }
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    single_product = Items.objects.get(category_table__slug = category_slug, slug = product_slug)
    context = {'single_product':single_product}

    return render(request,'product_detail.html',context)


def cart(request,total = 0, tax = 0, cart_items = None, grand_total = 0):
    custom_cart_id = None
    #fetching the cart items when the user is logged in
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user = request.user, is_active = True)

    else:     #fetching the cart items when the user is not logged in,since we are using get the cart is expecting a atleast one item, 
              #if there is no item in the cart use try and except block to avoid error
        try:  
            custom_cart_id = Cart.objects.get(cart_id = cart_id(request))
        except:
            pass    
        
        cart_items = CartItem.objects.filter(cart = custom_cart_id, is_active = True )

    if cart_items != None:
        for cart in cart_items:
            total += cart.Items.price * cart.quantity

        tax = ( 2 *total )/100
        grand_total = total + tax     

    context = {
            'total' : total,
            'cart_items' : cart_items,
            'tax': tax,
            'grand_total': grand_total
    }

    return render(request,'cart.html',context)

def addcart(request,proid):
    #passing the product id
    item = Items.objects.get(id = proid) 
    #if the product is present in cart we are fetching the item using session key
    try:                                 
        new_cart = Cart.objects.get(cart_id = cart_id(request))
    
    #if the product is not present in cart we are creating a new cart
    except Cart.DoesNotExist:           
        new_cart = Cart.objects.create(cart_id = cart_id(request))


    """this lines of code is for when the user is logged in and adding the items to the cart 
    if he had already added to the cart using a session key before loggin in"""
    if request.user.is_authenticated:  
        cart_item_exists = CartItem.objects.filter(Items=item,user = request.user).exists()
        #if there are any items in the cart
        if cart_item_exists:  
            cart_item_exists = CartItem.objects.filter(Items=item,user = request.user) 
            for item in cart_item:
               item.quantity += 1
               item.save()
        else:
            cart_item = CartItem.objects.create(
            Items = item,
            user = request.user,
            quantity = 1,
            is_active = True
            )
            cart_item.save()

    #if the user is not logged in add the item to the cart using session key 
    else:
        cart_item_exists = CartItem.objects.filter(Items=item,cart = new_cart).exists() 
        #if the item already exists increase the quantity  
        if cart_item_exists:   
            cart_item = CartItem.objects.filter(Items=item,cart = new_cart)

            for item in cart_item:
                item.quantity += 1
                item.save()
    
        #if the item does not exists in a cart create the item in cart
        else:                  
            cart_item = CartItem.objects.create(
                Items = item,
                cart = new_cart,
                quantity = 1,
                is_active = True
                )
            cart_item.save()

    return redirect('cart')


def cart_id(request):
    cartId = request.session.session_key

    if not cartId:
        cartId =  request.session.create()

    return  cartId  



def removecart_item(request,proid):         
    item = Items.objects.get(id = proid)
    try:

        #if the user is logged in remove the cart item based on user ID
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(Items = item, user = request.user)
        #if the user is not logged in, remove the cart item based on session key
        else:    
            custom_cart = Cart.objects.get(cart_id = cart_id(request))
            cart_item = CartItem.objects.get(Items = item, cart = custom_cart)
    except:
        pass
    
    cart_item.delete()   


def increment_cartItem(request, proid):
    try:
        #if the user is logged in remove the cart item based on user ID
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(Items = item, user = request.user)
        #if the user is not logged in, remove the cart item based on session key
        else:    
            custom_cart = Cart.objects.get(cart_id = cart_id(request))
            cart_item = CartItem.objects.get(Items = item, cart = custom_cart)
    except:
        pass

        cart_items.quantity += 1
        return redirect('cart')

def decrement_cartItem(request, proid):
    try:
        #if the user is logged in remove the cart item based on user ID
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(Items = item, user = request.user)
        #if the user is not logged in, remove the cart item based on session key
        else:    
            custom_cart = Cart.objects.get(cart_id = cart_id(request))
            cart_item = CartItem.objects.get(Items = item, cart = custom_cart)
    except:
        pass
    
    if cart_items.quantity > 1:    
        cart_items.quantity -= 1
    else:
        cart_item.delete()  

    return redirect('cart')

def checkout(request,total=0, tax=0, grand_total=0, cart_items=None):
   custom_cart_id = None
   if request.user.is_authenticated:
     cart_items = CartItem.objects.filter(user=request.user,is_active=True)
   else:
    try:
        custom_cart_id = Cart.objects.get(cart_id = cart_id(request))
        
    except:
        pass
    cart_items = CartItem.objects.filter(cart=custom_cart_id,is_active=True)
   

   if cart_items!= None:
    for cart_item in cart_items:
        total += cart_item.Items.price * cart_item.quantity

    
   tax = (2 * total)/100
   grand_total = total + tax

   context = {
            'total':total,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total

    }

   return render(request,'checkout.html',context)