from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Shop)
admin.site.register(models.Review)
admin.site.register(models.Comment)
admin.site.register(models.Images)
