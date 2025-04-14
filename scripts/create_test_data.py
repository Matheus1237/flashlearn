import os
import django
import random
from faker import Faker

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Deck, Card, UserProfile

# Criar Faker para dados aleatórios
fake = Faker('pt_BR')

def create_test_data():
    # Obter ou criar usuário
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'matheus@example.com'}
    )
    
    # Garantir que o usuário é Pro
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'is_pro': True})
    profile.is_pro = True
    profile.save()
    
    # Lista de assuntos principais
    main_subjects = [
        'Matemática', 'Física', 'Química', 'Biologia', 'História',
        'Geografia', 'Português', 'Inglês', 'Programação', 'Filosofia',
        'Sociologia', 'Artes', 'Música', 'Literatura', 'Economia'
    ]
    
    # Lista de subtópicos para cada assunto
    subtopics = {
        'Matemática': ['Álgebra', 'Geometria', 'Trigonometria', 'Cálculo', 'Estatística'],
        'Física': ['Mecânica', 'Termodinâmica', 'Eletromagnetismo', 'Óptica', 'Quântica'],
        'Química': ['Orgânica', 'Inorgânica', 'Físico-Química', 'Analítica', 'Bioquímica'],
        'Biologia': ['Genética', 'Ecologia', 'Anatomia', 'Botânica', 'Zoologia'],
        'História': ['Antiga', 'Medieval', 'Moderna', 'Contemporânea', 'Brasil'],
        'Geografia': ['Física', 'Humana', 'Política', 'Econômica', 'Brasil'],
        'Português': ['Gramática', 'Literatura', 'Redação', 'Interpretação', 'Linguística'],
        'Inglês': ['Grammar', 'Vocabulary', 'Speaking', 'Writing', 'Reading'],
        'Programação': ['Python', 'JavaScript', 'Java', 'C++', 'SQL'],
        'Filosofia': ['Ética', 'Lógica', 'Metafísica', 'Epistemologia', 'Política'],
        'Sociologia': ['Teoria', 'Cultura', 'Política', 'Trabalho', 'Educação'],
        'Artes': ['Pintura', 'Escultura', 'Música', 'Teatro', 'Cinema'],
        'Música': ['Teoria', 'História', 'Instrumentos', 'Composição', 'Harmonia'],
        'Literatura': ['Brasileira', 'Portuguesa', 'Inglesa', 'Americana', 'Universal'],
        'Economia': ['Micro', 'Macro', 'Internacional', 'Monetária', 'Desenvolvimento']
    }
    
    # Criar decks para cada assunto e subtópico
    for subject in main_subjects:
        for subtopic in subtopics[subject]:
            deck_name = f"{subject} - {subtopic}"
            deck = Deck.objects.create(
                user=user,
                name=deck_name,
                description=fake.paragraph(),
                is_public=random.choice([True, False])
            )
            
            # Criar entre 30 e 50 cards para cada deck
            num_cards = random.randint(30, 50)
            for _ in range(num_cards):
                Card.objects.create(
                    deck=deck,
                    front=fake.sentence(),
                    back=fake.paragraph()
                )
            
            print(f"Criado deck '{deck_name}' com {num_cards} cards")

if __name__ == '__main__':
    create_test_data() 