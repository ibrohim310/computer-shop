from django.contrib import admin
from main import models

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Enter)
admin.site.register(models.Out)
admin.site.register(models.Return)