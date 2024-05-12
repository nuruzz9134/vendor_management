from django.contrib import admin
from app.models import Vendors, PurchaseOrder , HistoricalPerformance

# Register your models here.

@admin.register(Vendors)
class VendorsModeladmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Vendors._meta.fields
        ]

@admin.register(PurchaseOrder)
class PurchaseOrderModeladmin(admin.ModelAdmin):
    list_display = [
        field.name for field in PurchaseOrder._meta.fields
        ]

@admin.register(HistoricalPerformance)
class HistoricalPerformanceModeladmin(admin.ModelAdmin):
    list_display = [
        field.name for field in HistoricalPerformance._meta.fields
        ]


