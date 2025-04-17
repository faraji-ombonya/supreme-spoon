from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Status
from .serializers import StatusSerializer


class StatusList(APIView):
    def get(self, request):
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StatusDetail(APIView):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status)
        return Response(serializer.data)

    def put(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
