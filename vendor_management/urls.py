
from django.contrib import admin
from app.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('POST /api/vendors/',CreateNewVendor.as_view(),name='create_new_vendor'),
    path('GET /api/vendors/',VendorsList.as_view(),name='vendors_list'),
    path('GET /api/vendors/<slug:pk>/',SingleVendor.as_view(),name='single_vendor'),


    path('POST /api/purchase_orders/',NewOrder.as_view(),name='new_order'),
    path('GET /api/purchase_orders/',OrderList.as_view(),name='order_list'),
    path('GET /api/purchase_orders/<slug:pk>/',SingleOrder.as_view(),name='single_order'),
    path('PUT /api/purchase_orders/<slug:pk>/',UpdateOrder.as_view()),

    path('GET /api/vendors/<slug:pk>/performance/',VendorPreformance.as_view()),
    path('POST /api/purchase_orders/<slug:pk>/acknowledge/',UpdateAcknowledgmentDate.as_view()),


    path('api-token-auth/', obtain_auth_token,name='token_obtain_pair')
]
