from django.urls import path

from .import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.CategoriesView.as_view(),name='categories'),
    # path('product/',views.ProductiesView.as_view(),name='products'),
    path('products/<int:category_id>/', views.ProductiesView.as_view(), name='products')


]  
if settings.DEBUG:
    urlpatterns += static(prefix = settings.MEDIA_URL, document_root =settings.MEDIA_ROOT )
    urlpatterns += static(prefix = settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    