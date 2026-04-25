from django.db import models

# Create your models here.

# Models Explaination :- 00:48:00
# one-to-many relationship between Product(title, description, unit_price, inventory, updated_at,collection, promotions) and Collection(title, featured_product)
# many-to-many realtionship between Product and Cart(created_at) 
# CartItem(quantity) is representing the many-to-many relationship between Product and Cart through quantity attribute, it is call association class
# Instead of creating the CartItem model as association class of Product and Cart, We can also create one-to-many relationship between (Product and CartItem) and (Cart and CartItem)
# one-to-many relationship between Customer(name,email) and Order(placed_at)
# many-to-many relationship between Order and Product, OrderItem(quantity) will be association class or we can create one-to-many relationship between (Product and OrderItem) and (Order and OrderItem) like we did in CartItem
# the store and tag are two different apps and we will be creating zero coupling between these apps.
# many-to-many relationship between Product and Tag(label), TagITem(quantity) will be association class

# We specify parent in the child class while creating relationships 

# Django Field Types : https://docs.djangoproject.com/en/6.0/ref/models/fields/
# Django Model Metadata: https://docs.djangoproject.com/en/6.0/ref/models/options/


class Promotion(models.Model):
    desctiption = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)

    ############### Circular Dependency/ Reverse Relationship : Product and Collections ###############    
    # featured_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99
    inventory = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    ############### Creating One-To-Many Relationship #############
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    ############### Creating Many-To-Many Relationship #############
    promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20) 
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


############ Order ###################
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)

    ############### Creating One-To-Many Relationship #############
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    ############### Creating One-To-Many Relationship #############
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    ############### Creating One-To-One Relationship #############
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)    # primary_key aregument will create one-to-one relationship

    ############### Creating One-To-Many Relationship #############
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    zip_code = models.CharField(max_length=6, default='999999')

########## Cart ############
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    ############### Creating One-To-Many Relationship #############
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    
