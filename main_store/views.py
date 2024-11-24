from django.db.models import Q
from django.views.generic import ListView

from .models import Product, Categories


# Create your views here.

class CustomRangeForPagination:
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

    
        paginator = context['paginator']
        page_obj = context ['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1

        if right_index >  page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages


        custom_range  = range(left_index,right_index +1)
        context['custom_range'] = custom_range




        return context
    
class CategoriesView(ListView):
    objects = None
    model = Categories
    template_name = 'main_store/categories.html'
    context_object_name = 'categories' 
    paginate_by = 2

    # def get_queryset(self):
    #     search = self.request.GET.get('q', '')
    #
    #     if search:
    #         return CategoriesView.objects.filter(
    #             Q(title__icontains=search) | Q(description__icontains=search)
    #         )
    #     else:
    #         return CategoriesView.objects.all()


class ProductiesView(ListView):
    template_name = "main_store/index.html"
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category__id=self.kwargs.get("category_id"))


