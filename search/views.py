from products.models import Product
from django.views.generic.list import ListView
from django.db.models import Q
# Create your views here.


class ProductSearchView(ListView):
    template_name = 'search/view.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('search', "Shirt")
        check = method_dict.get('indesc', None)
        if query is not None:
            if check:
                return Product.objects.filter(
                    Q(description__icontains=query) | 
                    Q(title__icontains=query) |
                    Q(tag__title__icontains=query)).distinct()
            return Product.objects.filter(title__icontains=query)
        return Product.objects.none()