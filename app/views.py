from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from app.serializers import *
import datetime
from django.utils import timezone


class CreateNewVendor(APIView):
    def post(self, request):
        try:
           unique_vendor_code = str(uuid.uuid4())[:8]
           request.data['vendor_code'] = unique_vendor_code
           serializer = VendorSerializers(
               data=request.data
               )
           if serializer.is_valid():
               serializer.save()
               return Response({'message':serializer.data}
                                ,status=status.HTTP_201_CREATED)
           else:
               return Response(repr(serializer.errors)
                               ,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response (
                {'message': str(e)}
                ,status=status.HTTP_400_BAD_REQUEST)
        

        
class VendorsList(APIView):
    def get(self, request):
        try:
            all_data = Vendors.objects.all()
            serializer = VendorSerializers(all_data,many=True)
            return Response({'message':serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'message':repr(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )



class SingleVendor(APIView):

    def get(self, request, pk):
        try:
            if Vendors.objects.filter(vendor_code=pk).exists():
                vendor_data = Vendors.objects.filter(vendor_code=pk)
                serializer = VendorSerializers(vendor_data,many=True)
                return Response({'massage':serializer.data}, 
                                status=status.HTTP_200_OK)
            else:
                return Response(
                        {'message':'vendor does not existed'}
                    , status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )
    

    def put(self, request, pk):
        try:
            if Vendors.objects.filter(vendor_code=pk).exists():
                vendor = Vendors.objects.get(vendor_code=pk)
                serializer = VendorSerializers(vendor,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {'message':'vendor data updated'}
                    , status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors)
            else:
                return Response(
                        {'message':'vendor does not existed'}
                    , status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )
        

    def delete(self, request, pk):
        try:
            if Vendors.objects.filter(vendor_code=pk).exists():
                vendor = Vendors.objects.get(vendor_code=pk)
                vendor.delete()
                return Response({'message':'vendor deletd'}, 
                                status=status.HTTP_200_OK)
            else:
                return Response(
                        {'message':'vendor does not existed'}
                    , status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )
        


class NewOrder(APIView):
    def post(self,request):
        try:
            request.data['vendor'] = request.user.id
            request.data['po_number'] = str(uuid.uuid4())[:10]
            serializer = PurchaseOrderSerializers(
               data=request.data
               )
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'new order created'}
                                    ,status=status.HTTP_201_CREATED)
            else:
                return Response(repr(serializer.errors)
                                ,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )
        


class OrderList(APIView):
    def get(self,request):
        permission_classes = (IsAuthenticated,)
        try:
            vendorID = request.user.id
            all_items = PurchaseOrder.objects.filter(vendor_id = vendorID)
            serializer = PurchaseOrderSerializers(all_items,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}
                            ,status=status.HTTP_400_BAD_REQUEST)



class SingleOrder(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
        try:
            if PurchaseOrder.objects.filter(po_number=pk).exists():
                item = PurchaseOrder.objects.filter(po_number=pk)
                serializer = PurchaseOrderSerializers(item,many=True)
                return Response(serializer.data
                                ,status=status.HTTP_200_OK)
            else:
                return Response({'message':'invalid order id'})
        except Exception as e:
            return Response({'message':str(e)}
                            ,status=status.HTTP_400_BAD_REQUEST)
        


class UpdateOrder(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk):
        try:
            if PurchaseOrder.objects.filter(
                po_number=pk).exists():
                po = PurchaseOrder.objects.get(
                    vendor = request.user.id,
                    po_number = pk
                )
                serializer = PurchaseOrderSerializers(
                    po,
                    data=request.data,
                    partial=True
                    )
                if serializer.is_valid():
                    serializer.save()
                    if serializer.data['status'] == 'completed':

                        delivered_po = PurchaseOrder.objects.filter(
                            vendor_id = request.user.id,
                            status = 'completed'
                        )
                        total_delivered_po = delivered_po.count()

                        ontime_delivery = 0
                        total_quality_rate = 0
                        number_of_quality_feedback = 0
                        total_issued_po = 0
                        delivery_completed_at = datetime.date.today()

                        for i in delivered_po:

                            if i.delivery_date.date() >= delivery_completed_at:
                                ontime_delivery += 1

                            if i.quality_rating is not None:
                                number_of_quality_feedback += 1
                                total_quality_rate += i.quality_rating

                            if i.issue_date is not None:
                                total_issued_po += 1
                
                        on_time_delivery_rate = ontime_delivery / total_delivered_po if total_delivered_po != 0 else ontime_delivery
                        average_quality_rating = total_quality_rate / number_of_quality_feedback if number_of_quality_feedback != 0 else total_quality_rate
                        fulfillment_rate = total_delivered_po / total_issued_po if total_issued_po != 0 else total_delivered_po

                        Vendors.objects.filter(
                                        id = request.user.id
                                    ).update(
                                        on_time_delivery_rate = on_time_delivery_rate,
                                        quality_rating_avg = average_quality_rating,
                                        fulfillment_rate = fulfillment_rate
                                    )
                        HistoricalPerformance.objects.create(
                                vendor_id = request.user.id,
                                date = datetime.date.today(),
                                on_time_delivery_rate = on_time_delivery_rate,
                                quality_rating_avg = average_quality_rating,
                                fulfillment_rate = fulfillment_rate
                            )

                        return Response(
                            {'message':'ordered data updated'}
                        , status=status.HTTP_200_OK)
                    return Response(
                        {'message':'ordered status updated, but not completed'}
                    , status=status.HTTP_200_OK)
                return Response(repr(serializer.errors)
                               ,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'invalid order id'})
        except Exception as e:
            return Response({'message':str(e)}
                            ,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            if PurchaseOrder.objects.filter(po_number=pk).exists():
                order = PurchaseOrder.objects.get(vendor_code=pk)
                order.delete()
                return Response({'message':'order deletd'}, 
                                status=status.HTTP_200_OK)
            else:
                return Response(
                        {'message':'order id does not existed'}
                    , status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )
        


class VendorPreformance(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        try:
            if HistoricalPerformance.objects.filter(
                vendor_id=request.user.id
                ).exists():
                v = Vendors.objects.get(vendor_code = pk)
                vendor_data = HistoricalPerformance.objects.filter(
                vendor_id=v
                )
                serializer = HistoricalPerformanceSerializers(
                vendor_data,many=True
                )

                return Response({'massage':serializer.data}, 
                                status=status.HTTP_200_OK)
            else:
                return Response(
                        {'message':'vendor does not existed'}
                    , status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response(
                {'message':str(e)}
                ,status=status.HTTP_400_BAD_REQUEST
            )




class UpdateAcknowledgmentDate(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,pk):
        try:
            if PurchaseOrder.objects.filter(
                po_number=pk).exists():
                po = PurchaseOrder.objects.get(
                    vendor = request.user.id,
                    po_number = pk
                )
                request.data['acknowledgment_date'] = request.data.get('acknowledgment_date')
                serializer = PurchaseOrderSerializers(
                    po,
                    data=request.data,
                    partial=True
                    )
                if serializer.is_valid():
                    serializer.save()
                    
                    all_po = PurchaseOrder.objects.filter(
                            vendor_id = request.user.id
                        )
                    total_po = all_po.count()

                    total_time_difference = 0

                    for i in all_po:
                        if  i.acknowledgment_date is not None and i.issue_date is not None:
                            time_difference = (i.acknowledgment_date - i.issue_date).total_seconds() / 3600
                            total_time_difference += time_difference 
                            
                    average_response_time = total_time_difference / total_po if total_po != 0 else total_time_difference
                        
                    Vendors.objects.filter(
                                        id = request.user.id
                                    ).update(
                                        average_response_time = average_response_time
                                    )
                    HistoricalPerformance.objects.create(
                                vendor_id = request.user.id,
                                date = datetime.date.today(),
                                average_response_time = average_response_time
                                )

                    return Response(
                            {'message':'ordered data updated'}
                        , status=status.HTTP_200_OK)
                return Response(repr(serializer.errors)
                               ,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'invalid order id'})
        except Exception as e:
            return Response({'message':str(e)}
                            ,status=status.HTTP_400_BAD_REQUEST)
        