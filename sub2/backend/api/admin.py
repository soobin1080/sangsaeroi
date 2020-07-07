from django.contrib import admin
from .models import LargeCategory, MediumCategory, SmallCategory, Area
# Register your models here.
admin.site.register(LargeCategory)
admin.site.register(MediumCategory)
admin.site.register(SmallCategory)
admin.site.register(Area)
