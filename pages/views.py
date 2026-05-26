from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from listings.choices import price_choices, bedroom_choices, state_choices
from listings.models import Listing
from listings.serializers import ListingSerializer
from realtors.models import Realtor
from realtors.serializers import RealtorSerializer


# Create your views here.
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def index(request):
    # 1. Fetch the data from the database
    listings = Listing.objects.order_by('-list_date').filter(
        is_published=True)[:3]

    # 2. Serialize the listings data for JSON responses only.
    serializer = ListingSerializer(listings, many=True)

    if request.accepted_renderer.format == 'html':
        return Response(
            {
                'listings': listings,
                'state_choices': state_choices,
                'bedroom_choices': bedroom_choices,
                'price_choices': price_choices,
            },
            template_name='pages/index.html'
        )

    return Response(
        {
            'listings': serializer.data,
            'state_choices': state_choices,
            'bedroom_choices': bedroom_choices,
            'price_choices': price_choices,
        }
    )


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')
    realtors_Serializers = RealtorSerializer(realtors, many=True)

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    mvp_Serializers = RealtorSerializer(mvp_realtors, many=True)

    if request.accepted_renderer.format == 'html':
        return Response(
            {
              'realtors': realtors,
              'mvp_realtors': mvp_realtors,
            },
            template_name='pages/about.html')

    return Response(
           {
              'realtors': realtors_Serializers.data,
              'mvp_realtors': mvp_Serializers.data,
           }
           )
