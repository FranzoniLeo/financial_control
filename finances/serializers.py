from rest_framework import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    total_balance = serializers.ReadOnlyField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'user', 'created_at', 'total_balance']
        read_only_fields = ['id', 'user', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'date', 'description', 
                 'wallet', 'wallet_name', 'created_at']
        read_only_fields = ['id', 'created_at']

