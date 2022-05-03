from django.urls import path
from . import views


urlpatterns = [
   
    path('productlist/',views.productlist.as_view()),
    path('showproduct/<int:pk>',views.showproduct.as_view()),
    path('productoffer/', views.productoffer.as_view()),
    path('categoryoffer/', views.Categoryoffer.as_view()),
    path('categoryitem/', views.categoryitem.as_view()),
]
