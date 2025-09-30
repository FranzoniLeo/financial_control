# 💰 Sistema de Controle Financeiro Pessoal

![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## 📋 Sobre o Projeto

Este é um **sistema de controle financeiro pessoal** desenvolvido em Django. O sistema permite que usuários gerenciem suas finanças pessoais através de carteiras digitais, categorias de investimentos e transações detalhadas.

### 🎯 Objetivos do Projeto
- **Aprendizado**: Aprimorar conhecimentos do framework Django
- **Prática**: Implementar funcionalidades reais de um sistema financeiro

## ✨ Funcionalidades Principais

### 🏦 Gestão de Carteiras
- ✅ Criação e gerenciamento de múltiplas carteiras
- ✅ Cálculo automático do saldo total
- ✅ Histórico de transações por carteira

### 📊 Categorias e Investimentos
- ✅ Sistema hierárquico de categorias (categorias e subcategorias)
- ✅ Gestão de investimentos por categoria
- ✅ Controle de saldo por investimento

### 💸 Transações Financeiras
- ✅ **Depósitos**: Adição de dinheiro às carteiras/investimentos
- ✅ **Saques**: Retirada de valores
- ✅ **Dividendos**: Recebimento de rendimentos
- ✅ Histórico completo com datas e descrições

### 👤 Sistema de Usuários
- ✅ Autenticação e autorização
- ✅ Perfis de usuário personalizados
- ✅ Isolamento de dados por usuário

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.5** - Framework web principal
- **Python 3.13** - Linguagem de programação
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização e responsividade
- **Django Templates** - Sistema de templates

### Ferramentas de Desenvolvimento
- **Git** - Controle de versão
- **Virtual Environment** - Isolamento de dependências
- **Django Admin** - Interface administrativa

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8+ instalado
- Git instalado

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/controle-financeiro.git
cd controle-financeiro
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute as migrações
```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

### 7. Acesse o sistema
- **Aplicação**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## 📱 Demonstração

### Dashboard Principal
O dashboard oferece uma visão geral das carteiras do usuário com:
- Lista de carteiras criadas
- Saldo total de cada carteira
- Ações rápidas (criar, editar, excluir)

### Gestão de Carteiras
- Interface intuitiva para criação de novas carteiras
- Edição e exclusão de carteiras existentes
- Visualização detalhada de cada carteira

### Sistema de Transações
- Formulários para registro de depósitos, saques e dividendos
- Histórico completo de transações
- Filtros por data e tipo de transação


## 📊 Modelos de Dados

### Wallet (Carteira)
- Vinculada a um usuário
- Nome personalizável
- Cálculo automático de saldo

### Category (Categoria)
- Sistema hierárquico (categorias e subcategorias)
- Vinculada a uma carteira

### Investment (Investimento)
- Vinculado a uma carteira e categoria
- Controle de saldo individual

### Transaction (Transação)
- Tipos: depósito, saque, dividendo
- Vinculada a carteira ou investimento
- Histórico completo com datas

## 🔧 Funcionalidades Técnicas Implementadas

- **Autenticação**: Sistema completo de login/logout
- **Validação**: Formulários com validação de dados
- **Agregações**: Cálculos automáticos de saldos
- **Templates**: Sistema de templates Django com herança
- **Static Files**: Gerenciamento de CSS e arquivos estáticos

## 🎓 Conceitos Django Aplicados

- **Models**: Definição de modelos com relacionamentos
- **Views**: Views baseadas em função com decorators
- **Forms**: Formulários Django com validação
- **Templates**: Sistema de templates com herança
- **Admin**: Interface administrativa personalizada
- **Authentication**: Sistema de autenticação integrado

## 🚧 Próximas Funcionalidades

- [ ] Gráficos e relatórios financeiros
- [ ] Exportação de dados (PDF/Excel)
- [ ] API REST com Django REST Framework
- [ ] Notificações por email
- [ ] Dashboard com métricas avançadas
- [ ] Integração com APIs de cotações
- [ ] Sistema de metas financeiras

