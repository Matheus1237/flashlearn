from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.deck_list, name='deck_list'),
    path('decks/search/', views.search_decks, name='search_decks'),
    path('decks/new/', views.create_deck, name='create_deck'),
    path('decks/<int:deck_id>/add-card/', views.add_card, name='add_card'),
    path('decks/<int:deck_id>/study/', views.study_deck, name='study_deck'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('deck/<int:deck_id>/editar/', views.edit_deck, name='edit_deck'),
    path('deck/<int:deck_id>/excluir/', views.delete_deck, name='delete_deck'),
    path('card/<int:card_id>/editar/', views.edit_card, name='edit_card'),
    path('card/<int:card_id>/excluir/', views.delete_card, name='delete_card'),
    path('deck/<int:deck_id>/cards/', views.deck_cards, name='deck_cards'),
    path('responder/<int:card_id>/', views.registrar_resposta, name='registrar_resposta'),
    path('decks/<int:deck_id>/desempenho/', views.desempenho_deck, name='desempenho'),
    path('decks/<int:deck_id>/desempenho-geral/', views.desempenho_geral_deck, name='desempenho_geral'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('upgrade-pro/', views.upgrade_to_pro, name='upgrade_pro'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('profile/', views.profile_view, name='profile'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
]
