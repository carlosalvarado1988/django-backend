from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

#This is similar to say admin.site.register(Product, ProductModelAdmin)
@register(Product)
class ProductIndex(AlgoliaIndex):
    # im commenting this line below to implement the settings key
    # should_index= 'is_public'
    Fields=[
        'title',
        'body',
        'price',
        'owner',
        'public',
    ]
    # this is a build in for the AlgoliaIndex library
    settings={
        'searchableAttributes': ['title', 'body'],
        'attributesForFaceting': ['owner', 'public']
    }
    tags= 'get_tags_list'