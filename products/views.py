from django.http.response import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    template_name = 'products/product_detail.html'
    queryset = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context["cart"] = cart_obj
        return context
    
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance =  Product.objects.get(slug=slug, active= True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm..")
        
        # Signal to analytics
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        
        return instance    
    
class ProductListView(ListView):
    template_name = 'products/product_list.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context["cart"] = cart_obj
        return context
    
    
    
# class ProductDetailView(DetailView):
#     template_name = 'products/product_detail.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         return Product.objects.filter(pk=pk)
    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = get_object_or_404(Product, pk=pk)
    #     return instance


# class FeaturedProductListView(ListView):
#     template_name = 'products/product_list.html'
#     queryset      = Product.objects.all().featured()

# class FeaturedProductDetailView(DetailView):
#     template_name = 'products/featured_detail.html'
    
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         return Product.objects.features().filter(pk=pk)