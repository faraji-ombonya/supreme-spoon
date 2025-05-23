from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import CylinderStatus, Cylinder, Customer, Order
from .serializers import (
    CylinderStatusSerializer,
    CreateCylinderStatusSerializer,
    AllocateCylinderSerializer,
    CustomerSerializer,
    CreateOrderSerializer,
    OrderSerializer,
    OrderResponseSerializer,
)
from .services import notify_customer
from utils.open_api import get_paginated_response_schema, page, per_page
from utils.pagination import paginate


@extend_schema(tags=["Cylinder Statuses"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                serializer_class=CylinderStatusSerializer,
                description="A paginated list of statuses.",
            ),
        },
    ),
    post=extend_schema(request=CreateCylinderStatusSerializer),
)
class CylinderStatusList(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = CylinderStatusSerializer

    def get(self, request: Request):
        cylinder_statuses = CylinderStatus.objects.all()
        response = paginate(
            qs=cylinder_statuses,
            serializer_class=self.serializer_class,
            request=request,
        )
        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = CreateCylinderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cylinder_status = serializer.save()

        # TODO: Update the gas level on the customer's profile
        bluetooth_id = cylinder_status.bluetooth_id
        serial_number = cylinder_status.serial_number

        try:
            cylinder = Cylinder.objects.get(
                bluetooth_id=bluetooth_id, serial_number=serial_number
            )
            cylinder.level_in_percent = cylinder_status.level_in_percent

            # If gas level is less than 10% send them an sms notification
            level = cylinder_status.level_in_percent
            if level < 6:
                name = (
                    cylinder.customer.first_name
                    or cylinder.customer.last_name
                    or "there"
                )

                notify_customer(
                    customer_id=cylinder.customer.id,
                    message=f"Hello {name}, We’ve detected that your gas level is down to 10%. To avoid any interruptions, we recommend scheduling a refill soon. Stay safe and stocked up!",
                )

            if 6 <= level <= 10:
                notify_customer(
                    customer_id=cylinder.customer.id,
                    message=f"Hi {name}, Your gas level has dropped below 5%, and a refill is urgently needed to avoid running out. Kindly place your order as soon as possible.",
                )

            cylinder.save()
        except Cylinder.DoesNotExist:
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Cylinder Statuses"])
class CylinderStatusDetail(APIView):
    serializer_class = CylinderStatusSerializer

    def get(self, request: Request, pk):
        cylinder_status = get_object_or_404(CylinderStatus, pk=pk)
        serializer = self.serializer_class(cylinder_status)
        return Response(serializer.data)

    def put(self, request: Request, pk):
        cylinder_status = get_object_or_404(CylinderStatus, pk=pk)
        serializer = self.serializer_class(cylinder_status, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk):
        cylinder_status = get_object_or_404(CylinderStatus, pk=pk)
        cylinder_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Allocate Cylinder"])
class AllocateCylinderView(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = AllocateCylinderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Customers"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                serializer_class=CustomerSerializer,
                description="A paginated list of customers.",
            ),
        },
    ),
    # post=extend_schema(request=CreateCylinderStatusSerializer),
)
class CustomerList(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = CustomerSerializer

    def get(self, request):
        customers = Customer.objects.all()
        response = paginate(
            qs=customers,
            serializer_class=self.serializer_class,
            request=request,
        )
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Customers"])
class CustomerDetail(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = CustomerSerializer

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Orders"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                serializer_class=OrderSerializer,
                description="A paginated list of orders.",
            ),
        },
    ),
    post=extend_schema(
        request=CreateOrderSerializer, responses=OrderResponseSerializer
    ),
)
class OrderList(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = CreateOrderSerializer

    def get(self, request):
        orders = Order.objects.all()
        response = paginate(
            qs=orders, serializer_class=OrderSerializer, request=request
        )
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order: Order = serializer.save()
        out_serializer = OrderResponseSerializer(instance=order)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Orders"])
class OrderDetail(APIView):
    serializer_class = OrderSerializer

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
