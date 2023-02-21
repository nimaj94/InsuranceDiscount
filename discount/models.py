import random

from django.conf import settings
from django.db import models
from django.db.models import Sum
from rest_framework import serializers

from django.conf import settings


class Discount(models.Model):
    amount = models.IntegerField()
    CASUALTY = 0
    COLLISION = 1
    TOI_CHOICES = (
        (CASUALTY, 'شخص ثالث'),
        (COLLISION, 'بدنه'),
    )
    type_of_insurance = models.SmallIntegerField(choices=TOI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @staticmethod
    def get_by_detail(type_of_insurance, user):
        return Discount.objects.get(type_of_insurance=type_of_insurance, user=user)

    @staticmethod
    def add(type_of_insurance, user):
        list_of_candidates = settings.DISCOUNT_CONF[type_of_insurance]['amounts']
        probability_distribution = settings.DISCOUNT_CONF[type_of_insurance]['probabilities']
        amount = random.choices(list_of_candidates, weights=probability_distribution, k=1)[0]
        return Discount.objects.create(amount=amount, type_of_insurance=type_of_insurance, user=user)

    @staticmethod
    def get_report():
        casualty = Discount.objects.extra(select={'hour': 'date_part(\'hour\', created_at)'})\
            .values('hour',)\
            .filter(type_of_insurance=Discount.CASUALTY)\
            .annotate(total=Sum('amount'),)\
            .order_by()
        collision = Discount.objects.extra(select={'hour': 'date_part(\'hour\', created_at)'}) \
            .values('hour', ) \
            .filter(type_of_insurance=Discount.COLLISION) \
            .annotate(total=Sum('amount'), ) \
            .order_by()
        return {'casualty': list(casualty), 'collision': list(collision)}


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['amount', 'type_of_insurance', 'created_at']
