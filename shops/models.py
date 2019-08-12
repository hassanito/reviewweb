from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.forms import ModelForm

import math

User = get_user_model()

# Create your models here.

class Shop(models.Model):
    handle = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    number_of_reviews =0
    cumulative = 0
    image = models.ImageField(upload_to='profile_image',default='default.jpg' ,blank=False)
    def __str__(self):
        return self.handle

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return str(self.id)
    def get_number_of_reviews(self):
        number = Review.objects.filter(reviewed_shop = self ).count()
        self.number_of_reviews= number
        return str(number)
    def get_cumulative_review(self):
        reviews = Review.objects.filter(reviewed_shop=self)
        number = reviews.count()
        cumulative =0
        for i in reviews:
            cumulative += i.rating
        if(number!=0):

            # truncate to 1 decimal number
            return '%.1f'%(cumulative/number)
        else:
            return 0
class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)

    reviewed_shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description

    def get_reviewer_pk(self):
        return reviewer.pk
from django.utils import timezone
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer','reviewed_shop','description']
