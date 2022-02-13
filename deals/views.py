from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework.response import Response
from .serializers import FileUploadSerializer, CustomerSerializer
from .models import Customer
from .services import save_file_to_bd


class DealsAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        serializer = CustomerSerializer
        customer = Customer.objects.all()[:5]
        data = serializer(customer, many=True).data
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            data, status = save_file_to_bd(file)
            cache.clear()
            return Response(data, status=status)
        else:
            return Response({"Status": "Error",
                             "Desc": "File not found"}, status=400)
