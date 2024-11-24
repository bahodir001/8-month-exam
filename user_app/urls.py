from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .import views
from .views import update_account

urlpatterns = [
    path('registration/',views.RegistrationView.as_view(), name='registration'),
    path('account/',views.AccountView,name='account'),
    path('login/',LoginView.as_view(template_name ='app_users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('account/cart/', views.CartView.as_view(), name='cart'),
    path('update-account/', update_account, name='update_account'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_product_card/<int:product_id>/', views.delete_product_card, name='delete_product_card'),
]