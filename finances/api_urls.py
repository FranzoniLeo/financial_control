from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import WalletViewSet, TransactionViewSet
from . import token_views

# Criar o router
router = DefaultRouter()

# Registrar os ViewSets
router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
    # Endpoints de autenticação por token
    path('generate-token/', token_views.generate_token, name='generate_token'),
    path('regenerate-token/', token_views.regenerate_token, name='regenerate_token'),
    path('delete-token/', token_views.delete_token, name='delete_token'),
]

# URLs automáticas criadas pelo router:
# GET    /api/wallets/                    - Lista todas as carteiras
# POST   /api/wallets/                    - Cria nova carteira
# GET    /api/wallets/{id}/               - Busca carteira específica
# PUT    /api/wallets/{id}/               - Atualiza carteira completa
# PATCH  /api/wallets/{id}/               - Atualização parcial
# DELETE /api/wallets/{id}/               - Remove carteira
# GET    /api/wallets/{id}/transactions/  - Transações da carteira
# POST   /api/wallets/{id}/add_transaction/ - Adiciona transação à carteira
# GET    /api/wallets/summary/            - Resumo das carteiras

# GET    /api/transactions/               - Lista todas as transações
# POST   /api/transactions/               - Cria nova transação
# GET    /api/transactions/{id}/          - Busca transação específica
# PUT    /api/transactions/{id}/          - Atualiza transação completa
# PATCH  /api/transactions/{id}/          - Atualização parcial
# DELETE /api/transactions/{id}/          - Remove transação
# GET    /api/transactions/by_type/?type=deposit - Filtra por tipo
# GET    /api/transactions/monthly_summary/ - Resumo mensal

# GET    /api/categories/                 - Lista todas as categorias
# POST   /api/categories/                 - Cria nova categoria
# GET    /api/categories/{id}/            - Busca categoria específica
# PUT    /api/categories/{id}/            - Atualiza categoria completa
# PATCH  /api/categories/{id}/            - Atualização parcial
# DELETE /api/categories/{id}/            - Remove categoria
# GET    /api/categories/by_wallet/?wallet_id=1 - Categorias por carteira

