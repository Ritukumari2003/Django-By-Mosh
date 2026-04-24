from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, DecimalField, Value, Func, Count, ExpressionWrapper    # Q For OR and AND operation in filter
# from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Customer, Product, OrderItem, Order
from tags.models import TaggedItem


def say_hello(request):
    ################## To retrieve all data ##################
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

    ################## To filter data ##################
    # query_set = Product.objects.filter(unit_price>20)   # Error
    # query_set = Product.objects.filter(unit_price_gt=20)
    # query_set = Product.objects.filter(unit_price__range=(20,30))
    # query_set = Product.objects.filter(collection__id__range=(1,2,3))
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__startswith='a')
    # query_set = Product.objects.filter(updated_at__year=2021)
    
    # ----------------------------------------------------------------------------

    ################## Additional complex queries : Q Objects ##################
    # 1. products : inventory<10 AND price<20
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__gt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__gt=20))

    # 2. products : inventory<10 OR price<20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))

    # ----------------------------------------------------------------------------
    ################## Additional complex queries : F Objects ##################
    # query_set = Product.objects.filter(inventory=F('collection__id'))

    # ----------------------------------------------------------------------------
    ################## Order By ##################
    # query_set = Product.objects.order_by('title')
    # query_set = Product.objects.order_by('unit_price','-title')
    # query_set = Product.objects.order_by('title').reverse()
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')

    # ----------------------------------------------------------------------------
    # query_set = OrderItem.objects.values('product_id').distinct()
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # query_set = Product.objects.only('id', 'title')   # Returns instance of the product table
    # query_set = Product.objects.defer('description') 
    
    # ---------------------------------------------------------------------------- 
    # select_related(1)
    # prefetch_related(n) 
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.select_related('collection').prefetch_related('promotions').all()

    # -----------------------------------------------------------------------------
    # Get the last 5 orders with their customer and items (incl products)
    # order = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # orderitem_set  : For reverse dependency 
    # query_set = Product

    # -----------------------------------------------------------------------------
    ################### Aggregate functions ##################
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))

    # -----------------------------------------------------------------------------
    # Expressions in Django: Value, F, Func, Aggregate 
    ################### Annotate ##################
    # query_set = Customer.objects.annotate(is_new=Value(True))
    # query_set = Customer.objects.annotate(new_id=F('id')+1)
    # query_set = Customer.objects.annotate(
    #     full_name = Func(F('first_name', Value(' '), F('last_name'), function='CONCAT'))
    # )
    # query_set = Customer.objects.annotate(fullname = Concat('first_name',Value(' '),'last_name'))

    # -----------------------------------------------------------------------------
    ################### Grouping Data ##################
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

    content_type = ContentType.objects.get_for_model(Product)
    query_set = TaggedItem.objects\
        .select_related('tag')\
        .filter(
            content_type=content_type,
            object_id=1
        )


    return render(request, 'hello.html', {
        'name': 'Joe', 
        # 'products': list(query_set),
        # 'orders': list(order),
        # 'result': result,
        'result' : list(query_set),
        })