from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from .models import Transaction
from .serializers import TransactionSerializer, CustomerSerializer, CustomerDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwnerOrAdmin
# Create your views here.

class TransactionView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_staff:
            return qs

        qs = qs.filter(customer = self.request.user)

        return qs
    
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(customer = self.request.user)

class TransactionDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]    

class TransactionViewModel(ModelViewSet): # union of ListCreateAPIView and RetrieveUpdateDestroyAPIView
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(customer = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_staff:
            return qs

        qs = qs.filter(customer = self.request.user)

        return qs
    
class CustomerView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

class CustomerDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        
        return super().get_serializer_class()