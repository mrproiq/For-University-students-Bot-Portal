from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Announcement
from telegram_bot.sender import send_announcement_to_telegram

@receiver(post_save, sender=Announcement)
def send_announcement_after_create(sender, instance, created, **kwargs):
    if created:  # faqat yangi e'lon yaratilganda
        send_announcement_to_telegram(instance)
