from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from shops.models import Shop,Comment,Review
import json

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("oh oh")
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)


# the autocomplete function comes from https://medium.com/@ninajlu/django-ajax-jquery-search-autocomplete-d4b4bf6494dd
def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Shop.objects.filter(handle__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.handle)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

from django.contrib.auth import authenticate

def logshit(request):
    if request.method=="POST":
        print("fuck this shit lol")
        print("HORY SHIT",request.POST)
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user is not None:
            print("authentication works")
    # A backend authenticated the credentials
        else:
            print("authentication does not work")
    # No backend authenticated the credentials
    return HttpResponse("FUCKLOL")

import json
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

def ajax_login(request):
    if request.method == 'POST':
        print("test login   ")
        login_form = AuthenticationForm(request, request.POST)
        response_data = {}
        # if login_form.is_valid():
        #     response_data['result'] = 'Success!'
        #     response_data['message'] = 'You"re logged in'
        # else:
        #     response_data['result'] = 'failed'
        #     response_data['message'] = 'You messed up'
        username= request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            print("login user")
            login(request, user)
            response_data['loggedin']= True
        else:
            response_data['loggedin']= False
            print("login failed")
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def comment(request):
    print("yayyyyy")
    response_data={}

    if request.method=="POST":
        print("user = ",request.user)
        print("review id = ",request.POST.get('review_id'))
        print("Text = ",request.POST.get('text'))
        user = request.user
        review_id = request.POST.get('review_id')
        text = request.POST.get('text')
        Comment.objects.create(
            review = Review.objects.get(id=review_id),
            author = user,
            text = text
        )
        response_data['loggedin']= True

    return HttpResponse(json.dumps(response_data), content_type="application/json")
from shops.models import Review,Shop
def review_ajax(request):
    response_data={}
    if request.method =='POST':
            print("Test this shit")
            reviewer = request.user
            reviewed_shop = request.POST.get('reviewed_shop')
            description = request.POST.get('review_text')
            rating = request.POST.get('rating')
            Review.objects.create(
                reviewer=reviewer,
                reviewed_shop=Shop.objects.get(id=reviewed_shop),
                description=description,
                rating=rating
            )
            response_data['loggedin']= True

    return HttpResponse(json.dumps(response_data), content_type="application/json")
