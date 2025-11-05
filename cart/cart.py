from django.contrib import messages
from django.utils.translation import gettext as _

from products.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=0, replace_current_quantity=False):
        """
        Add the specified product the cart if it exists
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('product successfully added to cart'))

        self.save()

    def remove(self, product):
        """
        Remove d product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('product successfully removed from cart'))
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].final_price * item['quantity']
            yield item

    def __len__(self):
        """
        Len product in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Clear product in cart
        """
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """
        Sum price products
        """
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['product_obj'].final_price for item in self.cart.values())
