from rest_framework import serializers
from .models import Wallet, Transaction, Category, Investment

class WalletSerializer(serializers.ModelSerializer):
    total_balance = serializers.ReadOnlyField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'user', 'created_at', 'total_balance']
        read_only_fields = ['id', 'user', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)
    investment_name = serializers.CharField(source='investment.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'date', 'description', 
                 'wallet', 'investment', 'wallet_name', 'investment_name', 'created_at']
        read_only_fields = ['id', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'wallet', 'created_at']
        read_only_fields = ['id', 'created_at']

class InvestmentSerializer(serializers.ModelSerializer):
    current_balance = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Investment
        fields = ['id', 'name', 'category', 'wallet', 'category_name', 
                 'current_balance', 'created_at']
        read_only_fields = ['id', 'created_at']
