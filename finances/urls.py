from django.urls import path
from . import views

urlpatterns = [
    path('wallet/', views.wallet, name='wallet'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("wallet/add/", views.add_wallet, name="add_wallet"),
    path('wallet/<int:wallet_id>/', views.wallet_detail, name='wallet_detail'),
    path('wallet/<int:wallet_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('wallet/<int:wallet_id>/edit-transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('wallet/<int:wallet_id>/delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]
