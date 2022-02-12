import csv, codecs
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileUploadSerializer, CustomerSerializer
from .models import Deal, Customer, Gems


class DealsAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    queryset = Customer.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        serializer = CustomerSerializer
        customer = Customer.objects.all()[:5]
        data = serializer(customer, many=True).data
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']

        csvfile = csv.DictReader(codecs.iterdecode(file, 'utf-8'))

        deals_list = []
        customer_list = []
        for row in csvfile:
            this_customer = Customer.objects.get_or_create(username=row['customer'])
            this_customer[0].spent_money += int(row['total'])
            this_gem = Gems.objects.get_or_create(gem=row['item'])[0]
            this_gem.username.add(this_customer[0])

            customer_list.append(this_customer[0])

            deals_list.append(
                Deal(
                    customer=this_customer[0],
                    item=row['item'],
                    total=row['total'],
                    quantity=row['quantity'],
                    date=row['date']
                )
            )
        Customer.objects.bulk_update(customer_list, fields=['spent_money'])
        Deal.objects.bulk_create(deals_list)

        return Response({'title': 'SomeData'})
