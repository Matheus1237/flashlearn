from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from core.models import UserProfile

class FreePlanLimitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            # Garante que o usuário tem um perfil
            try:
                profile = request.user.profile
            except:
                profile = UserProfile.objects.create(user=request.user)

            if request.path.startswith('/decks/new/') or request.path.endswith('/add-card/'):
                if not profile.is_pro:
                    deck_count = request.user.decks.count()
                    if request.path.startswith('/decks/new/') and deck_count >= 3:
                        messages.warning(request, 'Limite de 3 decks atingido. Faça upgrade para Pro!')
                        return redirect('deck_list')
                    
                    if request.path.endswith('/add-card/'):
                        deck_id = int(request.path.split('/')[-3])
                        card_count = request.user.decks.get(id=deck_id).cards.count()
                        if card_count >= 20:
                            messages.warning(request, 'Limite de 20 cards por deck atingido. Faça upgrade para Pro!')
                            return redirect('deck_list')

        response = self.get_response(request)
        return response 