# 💰 Sistema de Controle Financeiro

Um sistema completo de controle financeiro desenvolvido em Django, permitindo gerenciar carteiras, investimentos e transações de forma organizada e intuitiva.

## 🚀 Funcionalidades

### 📊 Dashboard Principal
- Visão geral de todas as carteiras do usuário
- Resumo financeiro com saldos e estatísticas
- Interface responsiva e moderna

### 💼 Gerenciamento de Carteiras
- Criar múltiplas carteiras personalizadas
- Editar e excluir carteiras existentes
- Visualizar detalhes de cada carteira

### 📈 Controle de Investimentos
- Organizar investimentos por categorias
- Categorias hierárquicas (categorias e subcategorias)
- Acompanhamento individual de cada investimento

### 💸 Gestão de Transações
- Registrar depósitos, saques e dividendos
- Histórico completo de transações
- Filtros por data e tipo de transação
- Cálculo automático de saldos

### 👤 Sistema de Usuários
- Cadastro e login de usuários
- Perfil personalizado
- Autenticação segura

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 5.2.5
- **Frontend:** HTML5, CSS3, JavaScript
- **Banco de Dados:** SQLite (desenvolvimento)
- **Autenticação:** Sistema nativo do Django
- **Interface:** Templates Django com CSS responsivo

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/controle-financeiro.git
cd controle-financeiro
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` no seu navegador.

## 📁 Estrutura do Projeto

```
controle-financeiro/
├── config/                 # Configurações do Django
│   ├── settings.py        # Configurações principais
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # Configuração WSGI
├── finances/             # App principal de finanças
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Lógicas de negócio
│   ├── forms.py          # Formulários
│   ├── urls.py           # URLs da app
│   └── templates/        # Templates HTML
├── users/                # App de usuários
│   ├── models.py         # Modelos de usuário
│   ├── views.py          # Views de autenticação
│   └── templates/        # Templates de login/cadastro
├── landing/              # App da página inicial
├── static/               # Arquivos estáticos (CSS, JS)
├── templates/            # Templates base
├── requirements.txt      # Dependências do projeto
└── manage.py            # Script de gerenciamento Django
```

## 🗄️ Modelos de Dados

### Wallet (Carteira)
- `user`: Usuário proprietário
- `name`: Nome da carteira
- `created_at`: Data de criação

### Category (Categoria)
- `wallet`: Carteira associada
- `name`: Nome da categoria
- `parent`: Categoria pai (para subcategorias)

### Investment (Investimento)
- `wallet`: Carteira associada
- `category`: Categoria do investimento
- `name`: Nome do investimento
- `created_at`: Data de criação

### Transaction (Transação)
- `investment`: Investimento associado (opcional)
- `wallet`: Carteira associada (opcional)
- `amount`: Valor da transação
- `transaction_type`: Tipo (deposit/withdrawal/dividend)
- `date`: Data da transação
- `description`: Descrição opcional

## 🎯 Como Usar

### 1. Primeiro Acesso
- Acesse a página inicial
- Clique em "Cadastrar" para criar uma conta
- Faça login com suas credenciais

### 2. Criando uma Carteira
- No dashboard, clique em "Nova Carteira"
- Digite um nome para sua carteira
- Confirme a criação

### 3. Gerenciando Investimentos
- Acesse uma carteira específica
- Crie categorias para organizar seus investimentos
- Adicione investimentos dentro das categorias

### 4. Registrando Transações
- Selecione um investimento ou carteira
- Clique em "Nova Transação"
- Preencha os dados (valor, tipo, data, descrição)
- Salve a transação

## 🔒 Segurança

- Autenticação obrigatória para todas as funcionalidades
- Cada usuário só acessa suas próprias carteiras e dados
- Validação de dados em formulários
- Proteção CSRF habilitada

## 🚀 Deploy em Produção

### Configurações Recomendadas

1. **Banco de Dados:** Configure PostgreSQL ou MySQL
2. **Variáveis de Ambiente:** Use `python-decouple` para configurações sensíveis
3. **Arquivos Estáticos:** Configure `whitenoise` ou serviço de CDN
4. **Servidor:** Use `gunicorn` para produção
5. **HTTPS:** Configure certificado SSL

### Exemplo de configuração para produção:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'controle_financeiro',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seuusuario](https://github.com/seuusuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seuperfil)

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique se seguiu todos os passos de instalação
2. Consulte a documentação do Django
3. Abra uma issue no GitHub
4. Entre em contato através do email: seuemail@exemplo.com

---

⭐ **Se este projeto te ajudou, considere dar uma estrela no GitHub!**
