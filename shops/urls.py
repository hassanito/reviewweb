from django.urls import path,include
from . import views
from .models import ReviewForm
app_name = 'shops'

urlpatterns=[
    path('',views.ListShops.as_view(),name='all'),
    path('<int:pk>', views.ShopDetail.as_view(), name='shop-detail'),
    path('<int:pk>/review/',views.review_create_view,name='review-shop'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),
    
    ]
