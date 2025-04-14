from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_pro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({'Pro' if self.is_pro else 'Free'})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    acertos = models.PositiveIntegerField(default=0)
    erros = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.front[:30]}..."
    

class SessaoEstudo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    inicio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.deck.name} - {self.inicio.strftime('%d/%m/%Y %H:%M')}"

class Resposta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='respostas')
    acertou = models.BooleanField()
    data_resposta = models.DateTimeField(auto_now_add=True)
    sessao = models.ForeignKey(SessaoEstudo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.card.front[:20]} - {'✅' if self.acertou else '❌'}"

