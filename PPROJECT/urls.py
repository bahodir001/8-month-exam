from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main_store.urls')),
    path('', include('user_app.urls'))

]
