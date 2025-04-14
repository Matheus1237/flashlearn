# FlashLearn

Sistema de aprendizado baseado em flashcards.

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as variáveis necessárias

5. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

7. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Deploy

O projeto está configurado para deploy no Render.com. Para fazer o deploy:

1. Crie uma conta no [Render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente no painel do Render
4. O deploy será automático após o push para a branch principal

## Tecnologias Utilizadas

- Django
- PostgreSQL
- Stripe (pagamentos)
- Bootstrap (frontend) 