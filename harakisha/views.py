from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .models import CylinderStatus
from .serializers import (
    CylinderStatusSerializer,
    CreateCylinderStatusSerializer,
    AllocateCylinderSerializer,
)
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
        serializer.save()

        # TODO: Update the gas level on the customer's profile
        # TODO: If gas level is less than 10% send them an sms notification
        # TODO: SMS has a URL that allows the user to place an order ()

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


# TODO:
# an endpoint that receives a QR code and customer details.
# Then use the QR code to query for the cylinder details
# Update customer profile


class AllocateCylinderView(APIView):
    serializer_class = AllocateCylinderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Query for the cylinder details using the QR code
        # Update customer profile
        # Allocate the cylinder to the customer

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# cylinder = Cylinder.objects.get(qr_code=qr_code)

# customer = Customer.objects.create(**customer_details)

# cylinder.customer = customer
# cylinder.save()

# return Response({"message": "Cylinder allocated successfully."})
