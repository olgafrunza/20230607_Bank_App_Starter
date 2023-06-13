from rest_framework import serializers
from .models import Transaction
from django.contrib.auth.models import User
from datetime import date

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
    
    def validate_amount(self, value):
        print("validation started")
        customer = self.context.get("request").user
        print(customer)
        trx = Transaction.objects.filter(customer = customer)
        
        current_balance = sum(i.amount for i in trx)
        print(current_balance, value)
        if current_balance + value < 0:
            raise serializers.ValidationError("Insufficient amount")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    days_passed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "days_passed")
    
    def get_days_passed(self, obj):
        registration_date = obj.date_joined.date()
        current_date = date.today()
        days_passed = (current_date - registration_date).days
        return days_passed

class CustomerDetailSerializer(serializers.ModelSerializer):
    # transactions = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    # transactions = serializers.StringRelatedField(many = True, read_only = True)
    transactions = TransactionSerializer(many = True, read_only = True)
    balance = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "balance", "transactions", )
    
    def get_balance(self, obj):
        trx = obj.transactions.all()
        # total = 0
        # for i in trx:
        #     total += i.amount
        total = sum(i.amount for i in trx)
        return total

