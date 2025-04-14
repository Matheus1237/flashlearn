from django.shortcuts import render, redirect
from .models import Deck, Card, Resposta, SessaoEstudo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .payments import create_checkout_session, handle_payment_success
from django.conf import settings
import stripe
from .models import UserProfile
from django.contrib import messages
from django.db.models import Q
from unidecode import unidecode
from django.urls import reverse

@login_required
def deck_list(request):
    search_query = request.GET.get('search', '')
    
    if request.user.profile.is_pro:
        decks = Deck.objects.filter(user=request.user)
    else:
        decks = Deck.objects.filter(user=request.user, is_active=True)
    
    if search_query:
        # Normalize the search query (remove accents and convert to lowercase)
        normalized_query = unidecode(search_query.lower())
        # Search in both original and normalized name
        decks = decks.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'core/deck_list.html', {
        'decks': decks,
        'search_query': search_query
    })

@login_required
def search_decks(request):
    search_query = request.GET.get('search', '').strip()
    
    if request.user.profile.is_pro:
        decks = Deck.objects.filter(user=request.user)
    else:
        decks = Deck.objects.filter(user=request.user, is_active=True)
    
    if search_query:
        # Normalize the search query (remove accents and convert to lowercase)
        normalized_query = unidecode(search_query.lower())
        # Search in both name and description
        decks = decks.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    results = []
    for deck in decks:
        results.append({
            'id': deck.id,
            'name': deck.name,
            'description': deck.description,
            'card_count': deck.cards.count(),
            'edit_url': reverse('edit_deck', args=[deck.id]),
            'delete_url': reverse('delete_deck', args=[deck.id]),
            'add_card_url': reverse('add_card', args=[deck.id]),
            'study_url': reverse('study_deck', args=[deck.id]),
            'performance_url': reverse('desempenho_geral', args=[deck.id]),
        })
    
    return JsonResponse({'results': results})

@login_required
def create_deck(request):
    if not request.user.profile.is_pro:
        active_decks = Deck.objects.filter(user=request.user, is_active=True).count()
        if active_decks >= 3:
            messages.error(request, 'Você atingiu o limite de decks do plano gratuito. Faça upgrade para o plano Pro para criar mais decks.')
            return redirect('deck_list')
            
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Deck.objects.create(user=request.user, name=name, description=description)
            return redirect('deck_list')
    return render(request, 'core/create_deck.html')

@login_required
def add_card(request, deck_id):
    deck = Deck.objects.get(id=deck_id, user=request.user)
    if request.method == 'POST':
        front = request.POST.get('front')
        back = request.POST.get('back')
        if front and back:
            Card.objects.create(deck=deck, front=front, back=back)
            return redirect('deck_list')
    return render(request, 'core/add_card.html', {'deck': deck})

@login_required
def study_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    if not request.user.profile.is_pro and not deck.is_active:
        messages.error(request, 'Este deck não está disponível no plano gratuito. Faça upgrade para o plano Pro para acessar todos os seus decks.')
        return redirect('deck_list')
        
    cards = deck.cards.all()
    sessao = SessaoEstudo.objects.create(user=request.user, deck=deck)

    return render(request, 'core/study_deck.html', {
        'deck': deck,
        'cards': cards,
        'sessao_id': sessao.id,
    })

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('deck_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('deck_list')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('deck_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def edit_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    if not request.user.profile.is_pro and not deck.is_active:
        messages.error(request, 'Este deck não está disponível no plano gratuito. Faça upgrade para o plano Pro para acessar todos os seus decks.')
        return redirect('deck_list')
        
    if request.method == 'POST':
        deck.name = request.POST.get('name')
        deck.description = request.POST.get('description')
        deck.save()
        return redirect('deck_list')
    return render(request, 'core/edit_deck.html', {'deck': deck})

@login_required
def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        deck.delete()
        return redirect('deck_list')
    return render(request, 'core/delete_deck.html', {'deck': deck})

@login_required
def edit_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, deck__user=request.user)
    if request.method == 'POST':
        card.front = request.POST.get('front')
        card.back = request.POST.get('back')
        card.save()
        return redirect('deck_list')
    return render(request, 'core/edit_card.html', {'card': card})

@login_required
def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, deck__user=request.user)
    if request.method == 'POST':
        card.delete()
        return redirect('deck_list')
    return render(request, 'core/delete_card.html', {'card': card})

@login_required
def deck_cards(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    if not request.user.profile.is_pro and not deck.is_active:
        messages.error(request, 'Este deck não está disponível no plano gratuito. Faça upgrade para o plano Pro para acessar todos os seus decks.')
        return redirect('deck_list')
        
    cards = deck.cards.all()
    return render(request, 'core/deck_cards.html', {'deck': deck, 'cards': cards})

@require_POST
@login_required
def registrar_resposta(request, card_id):
    print("Registrando resposta...")
    card = get_object_or_404(Card, id=card_id, deck__user=request.user)
    acertou = request.POST.get('acertou') == 'true'
    sessao_id = request.POST.get('sessao_id')

    sessao = get_object_or_404(SessaoEstudo, id=sessao_id, user=request.user)

    Resposta.objects.create(
        user=request.user,
        card=card,
        acertou=acertou,
        sessao=sessao
    )

    return JsonResponse({'status': 'ok'})

@login_required
def desempenho_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    ultima_sessao = SessaoEstudo.objects.filter(user=request.user, deck=deck).order_by('-inicio').first()

    if ultima_sessao:
        respostas = Resposta.objects.filter(sessao=ultima_sessao)
    else:
        respostas = Resposta.objects.none()

    acertos = respostas.filter(acertou=True).count()
    erros = respostas.filter(acertou=False).count()

    return render(request, 'core/desempenho.html', {
        'deck': deck,
        'acertos': acertos,
        'erros': erros,
        'sessao': ultima_sessao
    })

@login_required
def user_dashboard(request):
    total_decks = Deck.objects.filter(user=request.user).count()
    total_cards = Card.objects.filter(deck__user=request.user).count()
    
    respostas = Resposta.objects.filter(user=request.user)
    total_respostas = respostas.count()
    total_acertos = respostas.filter(acertou=True).count()
    total_erros = respostas.filter(acertou=False).count()
    
    taxa_acerto = (total_acertos / total_respostas * 100) if total_respostas > 0 else 0
    
    sessoes_recentes = SessaoEstudo.objects.filter(user=request.user).order_by('-inicio')[:5]
    
    desempenho_decks = []
    for deck in Deck.objects.filter(user=request.user):
        respostas_deck = Resposta.objects.filter(
            user=request.user,
            card__deck=deck
        )
        total_respostas_deck = respostas_deck.count()
        if total_respostas_deck > 0:
            acertos_deck = respostas_deck.filter(acertou=True).count()
            taxa_acerto_deck = (acertos_deck / total_respostas_deck * 100)
            desempenho_decks.append({
                'deck': deck,
                'total_respostas': total_respostas_deck,
                'acertos': acertos_deck,
                'erros': total_respostas_deck - acertos_deck,
                'taxa_acerto': taxa_acerto_deck
            })
    
    data_inicio = timezone.now() - timedelta(days=7)
    respostas_recentes = Resposta.objects.filter(
        user=request.user,
        data_resposta__gte=data_inicio
    )
    acertos_recentes = respostas_recentes.filter(acertou=True).count()
    erros_recentes = respostas_recentes.filter(acertou=False).count()
    
    return render(request, 'core/dashboard.html', {
        'total_decks': total_decks,
        'total_cards': total_cards,
        'total_respostas': total_respostas,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
        'taxa_acerto': taxa_acerto,
        'sessoes_recentes': sessoes_recentes,
        'desempenho_decks': desempenho_decks,
        'acertos_recentes': acertos_recentes,
        'erros_recentes': erros_recentes,
    })

@login_required
def upgrade_to_pro(request):
    if request.method == 'POST':
        price_id = 'price_1RDRi6GfUeWKkMq2KwurDo9r'
        session = create_checkout_session(request, price_id)
        if session:
            return JsonResponse({'sessionId': session.id})
        return JsonResponse({'error': 'Erro ao criar sessão de pagamento'}, status=400)
    
    return render(request, 'core/upgrade_pro.html', {
        'monthly_price': 9.90,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if handle_payment_success(session):
            return HttpResponse(status=200)
    
    return HttpResponse(status=200)

@login_required
def payment_success(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.is_pro = True
    user_profile.save()
    
    return render(request, 'core/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'core/payment_cancel.html')

@login_required
def desempenho_geral_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    respostas = Resposta.objects.filter(
        user=request.user,
        card__deck=deck
    )
    
    acertos = respostas.filter(acertou=True).count()
    erros = respostas.filter(acertou=False).count()
    
    total_sessoes = SessaoEstudo.objects.filter(
        user=request.user,
        deck=deck
    ).count()
    
    ultima_sessao = SessaoEstudo.objects.filter(
        user=request.user,
        deck=deck
    ).order_by('-inicio').first()

    return render(request, 'core/desempenho_geral.html', {
        'deck': deck,
        'acertos': acertos,
        'erros': erros,
        'total_sessoes': total_sessoes,
        'ultima_sessao': ultima_sessao
    })

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('profile')
        
    return render(request, 'core/profile.html')

@login_required
def cancel_subscription(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.is_pro = False
        user_profile.pro_expiration = None
        user_profile.save()
        
        # Get all decks and sort by creation date
        decks = Deck.objects.filter(user=request.user).order_by('-created_at')
        
        # If user has more than 3 decks, mark the excess ones as inactive
        if decks.count() > 3:
            for deck in decks[3:]:
                deck.is_active = False
                deck.save()
        
        messages.success(request, 'Sua assinatura foi cancelada com sucesso.')
        return redirect('profile')
    
    return render(request, 'core/cancel_subscription.html')
