from django.urls import path
from .views import TransactionView, TransactionDetail, TransactionViewModel, CustomerView, CustomerDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("transactions", TransactionViewModel)

urlpatterns = [
    path("trx/", TransactionView.as_view()),
    path("trx/<int:pk>/", TransactionDetail.as_view()),
    path("customer/", CustomerView.as_view()),
    path("customer/<int:pk>/", CustomerDetail.as_view()),
] + router.urls
