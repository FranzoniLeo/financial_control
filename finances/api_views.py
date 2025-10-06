from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

class WalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar carteiras.
    
    Endpoints automáticos:
    - GET /api/wallets/ - Lista todas as carteiras
    - POST /api/wallets/ - Cria nova carteira
    - GET /api/wallets/{id}/ - Busca carteira específica
    - PUT /api/wallets/{id}/ - Atualiza carteira completa
    - PATCH /api/wallets/{id}/ - Atualização parcial
    - DELETE /api/wallets/{id}/ - Remove carteira
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas carteiras do usuário logado"""
        return Wallet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automaticamente associa a carteira ao usuário logado"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """
        Endpoint customizado: GET /api/wallets/1/transactions/
        Retorna todas as transações de uma carteira específica
        """
        wallet = self.get_object()
        transactions = Transaction.objects.filter(wallet=wallet).order_by('-date', '-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_transaction(self, request, pk=None):
        """
        Endpoint customizado: POST /api/wallets/1/add_transaction/
        Adiciona uma nova transação à carteira
        """
        wallet = self.get_object()
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wallet=wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Endpoint customizado: GET /api/wallets/summary/
        Retorna resumo de todas as carteiras do usuário
        """
        wallets = self.get_queryset()
        total_balance = sum([w.get_total_balance() for w in wallets])
        
        return Response({
            'total_wallets': wallets.count(),
            'total_balance': total_balance,
            'wallets': WalletSerializer(wallets, many=True).data
        })

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar transações.
    
    Endpoints automáticos:
    - GET /api/transactions/ - Lista todas as transações
    - POST /api/transactions/ - Cria nova transação
    - GET /api/transactions/{id}/ - Busca transação específica
    - PUT /api/transactions/{id}/ - Atualiza transação completa
    - PATCH /api/transactions/{id}/ - Atualização parcial
    - DELETE /api/transactions/{id}/ - Remove transação
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas transações do usuário logado"""
        user = self.request.user
        return Transaction.objects.filter(
            Q(wallet__user=user)
        ).select_related('wallet').order_by('-date', '-created_at')
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Endpoint customizado: GET /api/transactions/by_type/?type=deposit
        Filtra transações por tipo
        """
        transaction_type = request.query_params.get('type')
        queryset = self.get_queryset()
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Endpoint customizado: GET /api/transactions/monthly_summary/
        Retorna resumo mensal das transações
        """
        from django.db.models import Sum
        from datetime import datetime
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        queryset = self.get_queryset().filter(
            date__month=current_month,
            date__year=current_year
        )
        
        deposits = queryset.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawals = queryset.filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
        dividends = queryset.filter(transaction_type='dividend').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'month': current_month,
            'year': current_year,
            'deposits': deposits,
            'withdrawals': withdrawals,
            'dividends': dividends,
            'net_income': deposits + dividends - withdrawals,
            'total_transactions': queryset.count()
        })

