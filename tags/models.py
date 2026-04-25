from django.db import models
# from store.models import Product  # Creating dependency of tags app on the store app, Not a good approach
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
            content_type = ContentType.objects.get_for_model(obj_type, obj_id)
            return TaggedItem.objects\
                .select_related('tag')\
                .filter(
                    content_type=content_type,
                    object_id=1
                )

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length = 255)

class TaggedItem(models.Model):
    objects = TaggedItemManager()   # For Generic Query
    # What tag is applied to what object 
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # product = models.ForeignKey(Product) # Dependent on Product table of store app

    ################# Defining Generic Relationship: 1:26:00 ##################
    # Type (product, video, article): For table
    # Using ContentType for abstraction so that the tags app will not be directly dependent on the store app to get the data from store.models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID : For record
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

