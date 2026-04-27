from urllib.parse import urlencode
from django.contrib import admin, messages
from django.http import HttpRequest
from django.db.models import QuerySet, Count
from django.utils.html import format_html
from django.urls import reverse
from . import models

# Register your models here.
# Django Model Admin: https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#modeladmin-options

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
# --------------------------------------------------------------------
############ Will Require dependency for generic class implementation here ###############
# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem
#     extra = 1   # optional, adds empty rows

# --------------------------------------------------------------------
################# Customising the List Page: 03:59:22 ###############
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    # exclude = ['promotions']
    # readonly_fields = ['title']
    # inlines = [TagInline]
    list_display = ['title', 'unit_price','inventory_status', 'collection_title']
    list_editable = ['unit_price']
    ####### Adding filter to the List Page: 04:19:09 #######
    list_filter = ['collection', 'updated_at', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product): return product.collection.title 

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10: return 'Low'
        return 'OK'
    
    ######### Creating Custom Actions : 04:23:30 ##########
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

# --------------------------------------------------------------------
################# Overriding the query set: 04:09:10 ###############
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection): 
        ####### Providing links to the page : 04:12:00 #######
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
            )
        return format_html('<a href="{}"> {} </a>', url, collection.products_count)
         
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    ####### Adding Search to the List Page: 04:17:16 #######
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    search_fields = ['customer']


# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)