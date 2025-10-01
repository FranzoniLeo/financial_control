from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@api_view(['POST'])
def generate_token(request):
    """
    Gera um token de autenticação para o usuário
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username e password são obrigatórios'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'Token gerado com sucesso!'
        })
    else:
        return Response(
            {'error': 'Credenciais inválidas'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_token(request):
    """
    Regenera o token do usuário autenticado
    """
    # Deleta o token antigo
    Token.objects.filter(user=request.user).delete()
    
    # Cria um novo token
    token = Token.objects.create(user=request.user)
    
    return Response({
        'token': token.key,
        'message': 'Token regenerado com sucesso!'
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_token(request):
    """
    Deleta o token do usuário autenticado
    """
    Token.objects.filter(user=request.user).delete()
    
    return Response({
        'message': 'Token deletado com sucesso!'
    })


@login_required
def token_management(request):
    """
    Página para o usuário gerenciar seus tokens
    """
    token, created = Token.objects.get_or_create(user=request.user)
    
    context = {
        'token': token.key if token else None,
        'has_token': bool(token)
    }
    
    return render(request, 'finances/token_management.html', context)
