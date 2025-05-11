from django.contrib import admin

from .models import Cylinder, CylinderStatus, Customer, Order


admin.site.register(Cylinder)
admin.site.register(CylinderStatus)
admin.site.register(Customer)
admin.site.register(Order)
