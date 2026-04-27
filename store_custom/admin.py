from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.


# --------------------------------------------------------------------
############ Creating for generic class implementation ###############
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1   # optional, adds empty rows
# --------------------------------------------------------------------

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)