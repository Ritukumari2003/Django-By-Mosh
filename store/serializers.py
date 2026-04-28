from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')

#     ############## Creating new attribute in the serializers ##################
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     ############## Searializing Relationships : 00:38:54 #################
#     # Using Primary Key
#     # Using String
#     # Using Nested Object
#     # Hyperlink
#     ######################
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )
#     # collection = serializers.StringRelatedField()
#     # collection = CollectionSerializer()
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal("1.1")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'   # Bad Practice
        fields = ['id', 'title', 'description','slug','inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal("1.1")
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other=1
    #     product.save()
    #     return product


    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data