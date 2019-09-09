from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from shops.models import Review,Shop
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect
import operator

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from shops.models import Shop
def slug_test(request, foo):
    print(foo)
    shop = Shop.objects.filter(handle=foo).get()
    url = shop.get_absolute_url()

    print(shop.get_absolute_url())
    return HttpResponseRedirect(reverse_lazy('shops:shop-detail',args=[shop.get_absolute_url()]))


class ListShops(generic.ListView):
    model = Shop
    paginate_by =2
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        if query:
            object_list = Shop.objects.filter(
                Q(handle__icontains=query) | Q(description__icontains=query)
                )
            return object_list
        else:
            object_list = Shop.objects.all()
            return object_list
    order_by ="-created_at"
class ShopDetail(generic.DetailView):
    model = Shop
    def get_context_data(self, *args, **kwargs):
        context = super(ShopDetail, self).get_context_data(*args, **kwargs)
        context['review_list'] = Review.objects.filter(reviewed_shop = self.get_object())
        return context

class ShopReviewsList(generic.ListView):
    model = Shop
    template_name ='shops/shops_reviews_list.html'
    paginate_by =2
    def get_context_data(self, *args, **kwargs):
        context = super(ShopReviewsList, self).get_context_data(*args, **kwargs)
        shop = get_object_or_404(Shop,pk=self.kwargs['pk'])
        context['shop'] = shop
        return context

    def get_queryset(self,*args,**kwargs): # new
        review_list =Review.objects.filter(reviewed_shop=self.kwargs['pk']).order_by("-created_at")
        return review_list

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def review_create_view(request,pk):

    value = request.POST.get('rating')
    shop = get_object_or_404(Shop,pk=pk)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.reviewed_shop = shop
        instance.reviewer = request.user
        instance.rating = value

        shop.number_of_reviews = shop.number_of_reviews +1
        shop.save()
        form.save()
        form = ReviewForm()

        return HttpResponseRedirect(reverse_lazy('shops:shop-detail',args=[pk]))
    context = {
        'form': form
    }
    return render(request,'shops/review_create.html',context)

# class ReviewEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Review
#     fields = ['description','rating']
#     value = request.POST.get('rating')
#     success_url = reverse_lazy('shops:all')
#
#     def form_valid(self, form):
#         form.instance.reviewer = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         review = self.get_object()
#         if self.request.user == review.reviewer:
#             return True
#         return False

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        pk = review.reviewed_shop.id
        if self.request.user == review.reviewer:

            return True
        return False
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        pk = self.get_object().reviewed_shop.id
        success_url = reverse_lazy('shops:shop-detail',args=[pk])
        self.object.delete()
        return HttpResponseRedirect(success_url)
