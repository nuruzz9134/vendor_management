from rest_framework import serializers
from app.models import *


class VendorSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Vendors.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    class Meta:
        model = Vendors
        fields = '__all__' 



class PurchaseOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__' 
    

class HistoricalPerformanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__' 