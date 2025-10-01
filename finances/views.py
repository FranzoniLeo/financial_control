from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.views.generic import TemplateView
from datetime import timedelta
from .forms import WalletForm
from .models import Wallet, Transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "finances/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Inicializa o formulário vazio por padrão
        context['form'] = WalletForm()
        
        # Todas as carteiras do usuário
        wallets = Wallet.objects.filter(user=user)
        context['wallets'] = wallets
        
        # Total de todas as carteiras
        total = sum([w.get_total_balance() for w in wallets])
        context['total'] = total
        
        # Todas as transações de rendimentos do usuário
        from django.db.models import Q
        transactions = Transaction.objects.filter(
            Q(investment__wallet__user=user, transaction_type="deposit") |
            Q(wallet__user=user, transaction_type="dividend")
        )
        
        # Rendimento total
        rendimento_total = transactions.aggregate(total_sum=models.Sum("amount"))["total_sum"] or 0
        context['rendimento_total'] = rendimento_total
        
        # Datas para filtros
        today = now().date()
        start_month = today.replace(day=1)
        last_month_end = start_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        start_year = today.replace(month=1, day=1)
        
        # Rendimento mês atual
        rendimento_mes_atual = transactions.filter(date__gte=start_month).aggregate(total_sum=models.Sum("amount"))["total_sum"] or 0
        context['rendimento_mes_atual'] = rendimento_mes_atual
        
        # Rendimento mês anterior
        rendimento_mes_anterior = transactions.filter(date__gte=last_month_start, date__lte=last_month_end).aggregate(total_sum=models.Sum("amount"))["total_sum"] or 0
        context['rendimento_mes_anterior'] = rendimento_mes_anterior
        
        # Rendimento no ano
        rendimento_ano = transactions.filter(date__gte=start_year).aggregate(total_sum=models.Sum("amount"))["total_sum"] or 0
        context['rendimento_ano'] = rendimento_ano
        
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        action = request.POST.get('action')
        
        if action == 'edit':
            return self._handle_edit_wallet(request, user)
        elif action == 'delete':
            return self._handle_delete_wallet(request, user)
        
        # Se não for uma ação conhecida, redireciona para GET
        return self.get(request, *args, **kwargs)
    
    def _handle_edit_wallet(self, request, user):
            wallet_id = request.POST.get('wallet_id')
            wallet_name = request.POST.get('name')
            
            try:
                wallet = get_object_or_404(Wallet, id=wallet_id, user=user)
                
                # Validar nome
                if not wallet_name or len(wallet_name.strip()) == 0:
                    return JsonResponse({'success': False, 'error': 'Nome da carteira é obrigatório'})
                
                if len(wallet_name.strip()) > 100:
                    return JsonResponse({'success': False, 'error': 'Nome da carteira deve ter no máximo 100 caracteres'})
                
                # Verificar se já existe outra carteira com o mesmo nome
                existing_wallet = Wallet.objects.filter(user=user, name=wallet_name.strip()).exclude(id=wallet_id)
                if existing_wallet.exists():
                    return JsonResponse({'success': False, 'error': 'Já existe uma carteira com este nome'})
                
                wallet.name = wallet_name.strip()
                wallet.save()
                
                return JsonResponse({'success': True, 'message': 'Carteira atualizada com sucesso!'})
                
            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Erro ao atualizar carteira'})
        
    def _handle_delete_wallet(self, request, user):
            wallet_id = request.POST.get('wallet_id')
            
            try:
                wallet = get_object_or_404(Wallet, id=wallet_id, user=user)
                wallet_name = wallet.name
                wallet.delete()
                
                return JsonResponse({'success': True, 'message': f'Carteira "{wallet_name}" excluída com sucesso!'})
                
            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Erro ao excluir carteira'})


# return finances/dashboard.html
@login_required
def wallet(request):
    return redirect('dashboard')


# return wallet form and save
@login_required
def add_wallet(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user  # associa ao usuário logado
            wallet.save()
            messages.success(request, f'Carteira "{wallet.name}" criada com sucesso!')
            return redirect("dashboard")  # volta para a página inicial
        else:
            # Se houver erros de validação, armazena na sessão e redireciona
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect("dashboard")
    else:
        return redirect("dashboard")


@login_required
def all_transactions_view(request):
    """
    View que mostra todas as transações usando a mesma estrutura do wallet_detail.html
    """
    user = request.user
    
    # Buscar todas as transações do usuário (de carteiras e investimentos)
    from django.db.models import Q
    transactions = Transaction.objects.filter(
        Q(wallet__user=user) | Q(investment__wallet__user=user)
    ).select_related('wallet', 'investment', 'investment__wallet').order_by('-date', '-created_at')
    
    # Calcular total geral (simulando uma carteira principal)
    total_balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'deposit':
            total_balance += float(transaction.amount)
        elif transaction.transaction_type == 'withdrawal':
            total_balance -= float(transaction.amount)
        elif transaction.transaction_type == 'dividend':
            total_balance += float(transaction.amount)
    
    # Criar um objeto "carteira virtual" para usar no template
    class VirtualWallet:
        def __init__(self, name, balance, transactions):
            self.name = name
            self.balance = balance
            self.transactions = transactions
        
        def get_total_balance(self):
            return f"{self.balance:.2f}"
    
    virtual_wallet = VirtualWallet("Todas as Carteiras", total_balance, transactions)

    context = {
        'wallet': virtual_wallet,
        'transactions': transactions,
        'is_all_transactions': True  # Flag para identificar que é a view de todas as transações
    }
    
    return render(request, "finances/wallet_detail.html", context)


@login_required
def wallet_detail(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    
    # Buscar todas as transações da carteira
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-date', '-created_at')
    
    context = {
        "wallet": wallet,
        "transactions": transactions,
    }
    return render(request, "finances/wallet_detail.html", context)


@login_required
def add_transaction(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    
    if request.method == "POST":
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')
        
        # Validações básicas
        if not transaction_type or not amount:
            messages.error(request, "Tipo de transação e valor são obrigatórios.")
            return redirect('wallet_detail', wallet_id=wallet_id)
        
        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "O valor deve ser maior que zero.")
                return redirect('wallet_detail', wallet_id=wallet_id)
        except ValueError:
            messages.error(request, "Valor inválido.")
            return redirect('wallet_detail', wallet_id=wallet_id)
        
        # Criar a transação
        try:
            # Mapear os tipos do formulário para os tipos do modelo
            type_mapping = {
                'income': 'deposit',
                'expense': 'withdrawal',
                'dividend': 'dividend'
            }
            
            transaction = Transaction.objects.create(
                wallet=wallet,
                transaction_type=type_mapping.get(transaction_type, 'deposit'),
                amount=amount,
                description=description,
                date=now().date()
            )
            
            messages.success(request, f"Transação de {transaction_type} no valor de R$ {amount:.2f} adicionada com sucesso!")
            
        except Exception as e:
            messages.error(request, f"Erro ao criar transação: {str(e)}")
    
    return redirect('wallet_detail', wallet_id=wallet_id)


@login_required
def edit_transaction(request, wallet_id, transaction_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    transaction = get_object_or_404(Transaction, id=transaction_id, wallet=wallet)
    
    if request.method == "POST":
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        
        # Validações básicas
        if not transaction_type or not amount or not date:
            messages.error(request, "Tipo de transação, valor e data são obrigatórios.")
            return redirect('wallet_detail', wallet_id=wallet_id)
        
        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "O valor deve ser maior que zero.")
                return redirect('wallet_detail', wallet_id=wallet_id)
        except ValueError:
            messages.error(request, "Valor inválido.")
            return redirect('wallet_detail', wallet_id=wallet_id)
        
        # Atualizar a transação
        try:
            # Mapear os tipos do formulário para os tipos do modelo
            type_mapping = {
                'income': 'deposit',
                'expense': 'withdrawal',
                'dividend': 'dividend'
            }
            
            transaction.transaction_type = type_mapping.get(transaction_type, 'deposit')
            transaction.amount = amount
            transaction.description = description
            transaction.date = date
            transaction.save()
            
            messages.success(request, f"Transação atualizada com sucesso!")
            
        except Exception as e:
            messages.error(request, f"Erro ao atualizar transação: {str(e)}")
    
    return redirect('wallet_detail', wallet_id=wallet_id)


@login_required
def delete_transaction(request, wallet_id, transaction_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    transaction = get_object_or_404(Transaction, id=transaction_id, wallet=wallet)
    
    if request.method == "POST":
        try:
            transaction.delete()
            messages.success(request, "Transação excluída com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao excluir transação: {str(e)}")
    
    return redirect('wallet_detail', wallet_id=wallet_id)