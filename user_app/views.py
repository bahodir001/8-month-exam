from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from main_store.models import Product
from .forms import UserRegistrationForm, UpdateAccountForm
from .models import UserModel, CartModels, Cart, CartItem


# from django.contrib.auth import authenticate, login
# from django.http import HttpResponseRedirect
# from django.views import View

class RegistrationView(CreateView):
    model = UserModel
    template_name = 'app_users/regstration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('categories')
    context_object_name = 'registration'


# class AccountView(CreateView):
#     model = UserModel
#     template_name = 'app_users/account.html'
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password1'])
#         user.save()
#         return super().form_valid(form)

def AccountView(request):
    return render(request, 'app_users/account.html')




def user_logout(request):
    logout(request)
    return redirect('categories')




@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.get_total_price() for item in items)
    shipping_cost = 0

    context = {
        'cart_items': items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': total_price + shipping_cost,
    }
    return render(request, 'app_product/cart.html', context)




class CartView(ListView):
    model = Cart
    template_name = 'app_product/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.total_price for item in context["cart_items"])
        context["total_price"] = total_price
        context["10_days_later"] = date.today() + timedelta(days=10)
        context["today"] = date.today()
        context["total_amount"] = total_price + 10
        return context




def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart.quantity += 1
        cart.save()

    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'app_product/cart.html', {'cart_items': cart_items})



def delete_product_card(request, product_id):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if cart_item.quantity <= 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')



@login_required
def update_account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = UpdateAccountForm(instance=request.user)

    return render(request, 'app_users/account.html', {'form': form})

