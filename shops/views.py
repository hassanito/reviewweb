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

class ListShops(generic.ListView):
    model = Shop

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

class ShopDetail(generic.DetailView):
    model = Shop
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def review_create_view(request,pk):

    value = request.POST.get('rating')
    print("helloooooooooooooooooooooooooooooooooooooo")
    print(value)
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
