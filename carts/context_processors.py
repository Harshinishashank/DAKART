from .models import Cart, CartItem
from DAKART.views import cart_id


def getCartItems(request):
    cart_count = 0
    cart_items = None
    try:
        #fetching the cart items based on session key
        custom_cart = Cart.objects.get(cart_id=cart_id(request))
        #fetching the cart items based on user if logged in
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user =request.user, is_active=True)
            cart_count = cart_items.count()
        #if the user is not logged in fetching the cart items based on session key    
        else:
            cart_items = CartItem.objects.filter(cart = custom_cart, is_active=True)   
            cart_count = cart_items.count()
             
    except Cart.DoesNotExist:
            pass
    
    return dict(count = cart_count)