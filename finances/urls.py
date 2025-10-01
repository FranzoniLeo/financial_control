from django.urls import path, include
from . import views
from . import token_views

urlpatterns = [
    # URLs das views tradicionais (Function Based Views e Class Based Views)
    path('wallet/', views.wallet, name='wallet'),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("wallet/add/", views.add_wallet, name="add_wallet"),
    path('all-transactions/', views.all_transactions_view, name='all_transactions'),
    path('wallet/<int:wallet_id>/', views.wallet_detail, name='wallet_detail'),
    path('wallet/<int:wallet_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('wallet/<int:wallet_id>/edit-transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('wallet/<int:wallet_id>/delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    
    # URLs de gerenciamento de tokens
    path('token-management/', token_views.token_management, name='token_management'),
    
    # URLs da API REST (ViewSets)
    path('api/', include('finances.api_urls')),
]
