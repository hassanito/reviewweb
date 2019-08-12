from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from shops.models import Shop
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
