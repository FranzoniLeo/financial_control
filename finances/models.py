from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=100, default="My Wallet")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wallet of {self.user.username}"
    
    def get_total_balance(self):
        # Calcular baseado nas transações diretas da carteira
        deposits = self.transactions.filter(transaction_type="deposit").aggregate(models.Sum("amount"))["amount__sum"] or 0
        withdrawals = self.transactions.filter(transaction_type="withdrawal").aggregate(models.Sum("amount"))["amount__sum"] or 0
        dividends = self.transactions.filter(transaction_type="dividend").aggregate(models.Sum("amount"))["amount__sum"] or 0
        return float(deposits - withdrawals + dividends)




class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=15,
        choices=[
            ("deposit", "Deposit"), 
            ("withdrawal", "Withdrawal"),
            ("dividend", "Dividend")
        ]
    )
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.wallet})"