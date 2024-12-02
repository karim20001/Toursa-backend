from datetime import date
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Tour, Purchase
from .serializers import TourSerializer

class CombinedHomeAPIView(APIView):
    """Returns Top Tours and Home Tours for the homepage."""

    def get(self, request):
        # Top 5 tours with the lowest remaining capacity
        top_tours = Tour.objects.filter(is_available=True).order_by('remaining_capacity')[:5]

        # Paginated tours ordered by start date
        home_tours = Tour.objects.filter(is_available=True).order_by('start_date')
        paginator = PageNumberPagination()
        paginator.page_size = 15  # Show 10 tours per page
        paginated_home_tours = paginator.paginate_queryset(home_tours, request)

        # Serialize both
        top_tours_serializer = TourSerializer(top_tours, many=True, context={'request': request})
        home_tours_serializer = TourSerializer(paginated_home_tours, many=True, context={'request': request})

        return paginator.get_paginated_response({
            "top_tours": top_tours_serializer.data,
            "home_tours": home_tours_serializer.data,
        })


class SearchTourAPIView(APIView):
    """View to search tours based on filters."""

    def get(self, request):
        queryset = Tour.objects.filter(is_available=True)  # Only available tours
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        transportation_type = request.GET.get('transportation_type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        passengers = request.GET.get('passengers')
        print(passengers)

        # Filter by search criteria
        if origin:
            queryset = queryset.filter(origin_city__icontains=origin)
        if destination:
            queryset = queryset.filter(destination_city__icontains=destination)
        if transportation_type:
            queryset = queryset.filter(transportation_type=transportation_type)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        if passengers:
            queryset = queryset.filter(remaining_capacity__gte=passengers)

        # Sort by most relevant (e.g., remaining capacity ascending + start date)
        queryset = queryset.order_by('remaining_capacity', 'start_date')

        # Paginate the results
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated_tours = paginator.paginate_queryset(queryset, request)

        # Serialize the data
        serializer = TourSerializer(paginated_tours, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class SingleTourAPIView(APIView):
    """Retrieve a single tour's details."""

    def get(self, request, pk):
        try:
            tour = Tour.objects.get(id=pk, is_available=True)
            serializer = TourSerializer(tour, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found or unavailable."}, status=status.HTTP_404_NOT_FOUND)


class CheckPurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        user = request.user
        tour = Tour.objects.get(id=pk)

        # Check if the tour is already purchased
        already_purchased = Purchase.objects.filter(user=user, tour=tour).exists()

        # Check if seats are available
        no_seats_left = tour.remaining_capacity == 0

        # Check if the tour date has passed
        tour_not_available = date.today() > tour.start_date

        return Response({
            "already_purchased": already_purchased,
            "no_seats_left": no_seats_left,
            "tour_not_available": tour_not_available
        })
    

class MyTravelsPagination(PageNumberPagination):
    page_size = 15  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class MyTravelsAPIView(APIView):
    """View to fetch user's purchased tours with pagination."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        purchases = Purchase.objects.filter(user=user).select_related('tour')
        tours = [purchase.tour for purchase in purchases]
        paginator = MyTravelsPagination()
        paginated_tours = paginator.paginate_queryset(tours, request)
        serializer = TourSerializer(paginated_tours, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)