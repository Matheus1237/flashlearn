# 🚀 FlashLearn

**Uma plataforma completa de flashcards para aprendizado eficiente e personalizado**

FlashLearn é uma aplicação web moderna desenvolvida em Django que permite aos usuários criar, gerenciar e estudar com flashcards de forma intuitiva e eficaz. A plataforma oferece um sistema de assinatura premium com funcionalidades avançadas de acompanhamento de desempenho.

## ✨ Funcionalidades Principais

### 🎯 Sistema de Estudos

- **Criação de Decks**: Organize seus flashcards em decks temáticos
- **Flashcards Dinâmicos**: Crie cards com frente e verso personalizáveis
- **Sessões de Estudo**: Sistema de estudo interativo com registro de respostas
- **Acompanhamento de Performance**: Métricas detalhadas de acertos e erros
- **Dashboard Personalizado**: Visão geral do progresso de aprendizado

### 💳 Sistema de Assinatura

- **Plano Gratuito**: Até 3 decks ativos e 20 cards por deck
- **Plano Pro**: Acesso ilimitado a todos os recursos
- **Pagamentos Seguros**: Integração com Stripe para processamento de pagamentos
- **Gerenciamento de Assinatura**: Upgrade e cancelamento simplificados

### 🔐 Autenticação e Segurança

- **Sistema de Login/Registro**: Autenticação personalizada
- **Perfis de Usuário**: Gerenciamento completo de dados pessoais
- **Middleware de Limites**: Controle automático de recursos por plano
- **Configurações de Segurança**: HTTPS, CSRF protection e validações

### 📊 Analytics e Relatórios

- **Estatísticas Gerais**: Taxa de acerto global e por deck
- **Histórico de Sessões**: Acompanhamento temporal do progresso
- **Performance por Deck**: Métricas específicas para cada conjunto de cards
- **Relatórios Recentes**: Análise dos últimos 7 dias

## 🛠️ Tecnologias Utilizadas

### Backend

- **Django 4.2.11** - Framework web robusto e escalável
- **SQLite** - Banco de dados para desenvolvimento e produção
- **Django ORM** - Mapeamento objeto-relacional
- **Stripe API** - Processamento de pagamentos
- **WhiteNoise** - Servindo arquivos estáticos

### Frontend

- **HTML5/CSS3** - Interface responsiva e moderna
- **JavaScript** - Interatividade e AJAX
- **Bootstrap** - Framework CSS para design responsivo
- **Templates Django** - Sistema de templates dinâmico

### DevOps e Deploy

- **Render** - Plataforma de deploy em nuvem
- **Gunicorn** - Servidor WSGI para produção
- **Python 3.11.7** - Linguagem de programação
- **Git** - Controle de versão

## 📁 Estrutura do Projeto

```
flashlearn/
├── core/                    # Aplicação principal
│   ├── models.py           # Modelos de dados (User, Deck, Card, etc.)
│   ├── views.py            # Lógica de negócio e views
│   ├── forms.py            # Formulários customizados
│   ├── middleware.py       # Middleware para controle de limites
│   ├── payments.py         # Integração com Stripe
│   ├── urls.py            # Rotas da aplicação
│   └── management/         # Comandos Django customizados
├── setup/                  # Configurações do projeto
│   ├── settings.py        # Configurações Django
│   └── urls.py           # URLs principais
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   └── core/             # Templates específicos
├── staticfiles/          # Arquivos estáticos
├── requirements.txt      # Dependências Python
└── render.yaml          # Configuração de deploy
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.11.7 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação Local

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/flashlearn.git
cd flashlearn
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

```bash
# Crie um arquivo .env na raiz do projeto
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
STRIPE_PUBLISHABLE_KEY=sua-chave-publica-stripe
STRIPE_SECRET_KEY=sua-chave-secreta-stripe
```

5. **Execute as migrações**

```bash
python manage.py migrate
```

6. **Crie um superusuário**

```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento**

```bash
python manage.py runserver
```

8. **Acesse a aplicação**

```
http://127.0.0.1:8000
```

## 🎯 Principais Modelos de Dados

### UserProfile

- Gerencia informações do usuário e status Pro
- Criado automaticamente para novos usuários

### Deck

- Representa um conjunto de flashcards
- Possui nome, descrição e status de ativação
- Limitado por plano de assinatura

### Card

- Flashcard individual com frente e verso
- Registra estatísticas de acertos e erros
- Pertence a um deck específico

### SessaoEstudo

- Registra sessões de estudo dos usuários
- Permite acompanhamento temporal do progresso

### Resposta

- Armazena respostas dos usuários durante o estudo
- Vinculada a sessões e cards específicos

## 💡 Destaques Técnicos

### Arquitetura

- **MVC Pattern**: Separação clara entre modelos, views e templates
- **Middleware Customizado**: Controle automático de limites por plano
- **Sistema de Signals**: Criação automática de perfis de usuário

### Segurança

- **CSRF Protection**: Proteção contra ataques CSRF
- **HTTPS Enforcement**: Redirecionamento automático para HTTPS em produção
- **Validação de Dados**: Validação robusta em formulários e modelos

### Performance

- **Queries Otimizadas**: Uso eficiente do ORM Django
- **Arquivos Estáticos**: Compressão e cache de assets
- **Banco de Dados**: Estrutura normalizada e indexada

### Integração de Pagamentos

- **Stripe Checkout**: Processamento seguro de pagamentos
- **Webhooks**: Atualização automática de status de assinatura
- **Gerenciamento de Erros**: Tratamento robusto de falhas de pagamento

## 📈 Métricas e Analytics

A plataforma coleta e apresenta diversas métricas importantes:

- **Taxa de Acerto Global**: Percentual de acertos em todas as respostas
- **Performance por Deck**: Estatísticas específicas por conjunto de cards
- **Sessões de Estudo**: Histórico completo de atividades
- **Progresso Temporal**: Análise de melhoria ao longo do tempo
- **Engagement**: Número de cards estudados e frequência de uso

## 🔧 Comandos de Desenvolvimento

```bash
# Criar dados de teste
python manage.py create_user_profiles

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Criar migrações
python manage.py makemigrations
```

## 🌐 Deploy em Produção

O projeto está configurado para deploy automático no **Render**:

- **Build Automático**: Integração com Git para builds contínuos
- **Variáveis de Ambiente**: Configuração segura de secrets
- **SSL Automático**: Certificados HTTPS gerenciados automaticamente
- **Escalabilidade**: Suporte a múltiplos workers

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

**FlashLearn** - Transformando o aprendizado em uma experiência eficiente e personalizada! 🎓✨
