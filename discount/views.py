import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Discount, DiscountSerializer


class DiscountView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        type_of_insurance = int(request.query_params['type_of_insurance'])
        try:
            discount = Discount.get_by_detail(type_of_insurance, user)
            result_status = status.HTTP_200_OK
        except ObjectDoesNotExist:
            discount = Discount.add(type_of_insurance, user)
            result_status = status.HTTP_201_CREATED
        return Response(DiscountSerializer(discount).data, status=result_status)


class ReportView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        report = Discount.get_report()
        print(report)
        return Response(json.dumps(report), status=status.HTTP_200_OK)
