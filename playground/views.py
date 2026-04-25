from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, DecimalField, Value, Func, Count, ExpressionWrapper    # Q For OR and AND operation in filter
# from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Collection, Customer, Product, OrderItem, Order
from tags.models import TaggedItem
from django.db import connection, transaction

# @transaction.atomic()
def say_hello(request):
    ################## To retrieve all data: 02:20:00 ##################
    # query_set = Product.objects.all()
    # 0,1,2,3,4
    # query_set = Product.objects.all()[0:5]
    # query_set = Product.objects.values('id', 'title', 'collection__title')
    # query_set = Product.objects.values_list('id', 'title', 'collection__title')

    ################## To retrieve data using primary key ##################
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # ----------------------------------------------------------------------------

    # product = Product.objects.filter(pk=0).first()
    # product_exists = Product.objects.filter(pk=0).exists()

    ################## To filter data : 02:30:47 ##################
    # query_set = Product.objects.filter(unit_price>20)   # Error
    # query_set = Product.objects.filter(unit_price_gt=20)
    # query_set = Product.objects.filter(unit_price__range=(20,30))
    # query_set = Product.objects.filter(collection__id__range=(1,2,3))
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__startswith='a')
    # query_set = Product.objects.filter(updated_at__year=2021)
    
    # ----------------------------------------------------------------------------

    ################## Additional complex queries : Q Objects: 02:38:15 ##################
    # 1. products : inventory<10 AND price<20
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__gt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__gt=20))

    # 2. products : inventory<10 OR price<20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))

    # ----------------------------------------------------------------------------
    ################## Additional complex queries : F Objects: 02:41:00 ##################
    # query_set = Product.objects.filter(inventory=F('collection__id'))

    # ----------------------------------------------------------------------------
    ################## Sorting: Order By: 02:42:20 ##################
    # query_set = Product.objects.order_by('title')
    # query_set = Product.objects.order_by('unit_price','-title')
    # query_set = Product.objects.order_by('title').reverse()
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')

    # ----------------------------------------------------------------------------
    ################## Selecting fields to queries: 02:47:31 ##################
    # Select products that have been ordered and sort them ny title: 02:49:50
    # query_set = OrderItem.objects.values('product_id').distinct()
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # query_set = Product.objects.only('id', 'title')   # Returns instance of the product table
    # query_set = Product.objects.defer('description') 

    # ---------------------------------------------------------------------------- 
    ################### Deferring fields : only and defer method in ORM : 02:53:37 ##################
    # ---------------------------------------------------------------------------- 
    
    # ---------------------------------------------------------------------------- 
    ################### Selecting related Queries: 02:56:52 ##################
    # select_related(1) - Creates join between the tables
    # prefetch_related(n) 
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.select_related('collection').prefetch_related('promotions').all()

    # -----------------------------------------------------------------------------
    # Get the last 5 orders with their customer and items (incl products)
    # order = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # orderitem_set  : For reverse dependency 
    # query_set = Product

    # -----------------------------------------------------------------------------
    ################### Aggregate functions: 03:06:05 ##################
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))

    # -----------------------------------------------------------------------------
    # Expressions in Django: Value, F, Func, Aggregate 
    ################### Annotate To add a new attribute in the table: 003:09:25 ##################
    # query_set = Customer.objects.annotate(is_new=Value(True))
    # query_set = Customer.objects.annotate(new_id=F('id'))
    # query_set = Customer.objects.annotate(new_id=F('id')+1)
    # query_set = Customer.objects.annotate(
    #     full_name = Func(F('first_name', Value(' '), F('last_name'), function='CONCAT'))
    # )
    # query_set = Customer.objects.annotate(fullname = Concat('first_name',Value(' '),'last_name'))

    # -----------------------------------------------------------------------------
    ################### Grouping Data: 03:15:50 ##################
    # query_set = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # -----------------------------------------------------------------------------
    ################### Expression Wrapper ##################
    # discounted_price = ExpressionWrapper(
    #     F('unit_price')*0.8, output_field=DecimalField()
    # )
    # query_set = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )

    # -----------------------------------------------------------------------------
    ################### Querying the generic classes : 03:19:00 ###################
    # content_type = ContentType.objects.get_for_model(Product)
    # query_set = TaggedItem.objects\
    #     .select_related('tag')\
    #     .filter(
    #         content_type=content_type,
    #         object_id=1
    #     )

    # -----------------------------------------------------------------------------
    ################### Custom Manager : 03:28:32 ###################
    # TaggedItem.objects.get_tags_for(Product,1)

    # -----------------------------------------------------------------------------
    ################### QuerySet Cache : 03:30:56 ###################
    # query_set = Product.objects.all()
    # list(query_set)  # Caching the query
    # query_set[0] # Retrieves data from cached query

    # -----------------------------------------------------------------------------
    ################### Creating/ Inserting Objects in the table : 03:33:25 ###################
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # collection = Collection.objects.create(name='Video Games', featured_product_id = 1)
    # collection.id

    # -----------------------------------------------------------------------------
    ################### Updating Objects in the table : 03:36:50 ###################
    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()

    # Collection.objects.filter(pk=11).update(featured_product_id = None)

    # -----------------------------------------------------------------------------
    ################### Deleting Objects in the table : 03:40:00 ###################
    # collection = Collection(pk=11)
    # collection.delete()

    # Collection.objects.filter(id__gt=5).delete()

    # -----------------------------------------------------------------------------
    ################### Transactions : 03:42:00 ###################
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # -----------------------------------------------------------------------------
    ################### Executing raw sql queries : 03:46:00 ###################
    # query_set = Product.objects.raw('SELECT id, title from store_product')
    # with connection.cursor() as cursor:
    #     cursor.execute('#Add Queries here#')


    return render(request, 'hello.html', {
        'name': 'Joe', 
        # 'products': list(query_set),
        # 'orders': list(order),
        # 'result': result,
        # 'result' : list(query_set),
        # 'tags' : list(query_set),
        })