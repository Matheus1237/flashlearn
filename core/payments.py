import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, price_id):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
            customer_email=request.user.email,
            metadata={
                'user_id': request.user.id
            }
        )
        return checkout_session
    except Exception as e:
        print(f"Erro ao criar sessão de checkout: {str(e)}")
        return None

def handle_payment_success(session):
    try:
        user_id = session.metadata.get('user_id')
        if user_id:
            user_profile = get_object_or_404(UserProfile, user_id=user_id)
            user_profile.is_pro = True
            user_profile.save()
            return True
    except Exception as e:
        print(f"Erro ao processar pagamento bem-sucedido: {str(e)}")
    return False 