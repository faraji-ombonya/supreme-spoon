"""
URL configuration for PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        "cylinder-statuses/",
        views.CylinderStatusList.as_view(),
        name="cylinder_status_list",
    ),
    path(
        "cylinder-statuses/<uuid:pk>/",
        views.CylinderStatusDetail.as_view(),
        name="cylinder_status_detail",
    ),
    path(
        "allocate-cylinder/",
        views.AllocateCylinderView.as_view(),
        name="allocate_cylinder",
    ),
    path("customers/", views.CustomerList.as_view(), name="customer_list"),
    path(
        "customers/<uuid:pk>/", views.CustomerDetail.as_view(), name="customer_detail"
    ),
    path("orders/", views.OrderList.as_view(), name="order_list"),
    path("orders/<uuid:pk>/", views.OrderDetail.as_view(), name="order_detail"),
]
