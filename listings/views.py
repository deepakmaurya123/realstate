from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing
from listings.serializers import ListingSerializer


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def index(request):
    listings = Listing.objects.order_by('id').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    paged_listings_Serializers = ListingSerializer(paged_listings, many=True)

    if request.accepted_renderer.format == 'html':
        return Response({'listings': paged_listings},
                        template_name='listings/listings.html')

    return Response({'listings': paged_listings_Serializers.data})


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing_Serializers = ListingSerializer(listing)

    if request.accepted_renderer.format == 'html':
        return Response({'listing': listing},
                        template_name='listings/listing.html')

    return Response({'listing': listing_Serializers.data})


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    print(request)
    print(queryset_list)

    queryset_list_Serializers = ListingSerializer(queryset_list, many=True)

    if request.accepted_renderer.format == 'html':
        return Response(
          {
            'state_choices': state_choices,
            'bedroom_choices': bedroom_choices,
            'price_choices': price_choices,
            'listings': queryset_list,
            'values': request.GET
          },
          template_name='listings/search.html'
        )

    return Response(
        {
          'state_choices': state_choices,
          'bedroom_choices': bedroom_choices,
          'price_choices': price_choices,
          'listings': queryset_list_Serializers.data,
          'values': request.GET
        }
    )
