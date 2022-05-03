from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
# from .views import CartView
from django.urls import include




# router = DefaultRouter()
# # router.register('',CartView)
# router.register(r'', CartView, basename="cart")
# urlpatterns = router.urls







urlpatterns=[

    path('usercart/',views.Viewcart.as_view(),name="cartview"),
    path('removeitem/<int:pk>',views.Viewcart.as_view(),name=""),
    path('additem/',views.AddCart.as_view(),name=""),
    path('couponcheck/', views.couponchecking.as_view(), name=""),
    path('copon/', views.couponapplay.as_view(), name=""),



    # path('', include(router.urls)),
   
    ]


