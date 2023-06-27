from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
# импортируем нужный декоратор
from django.dispatch import receiver
from django.template.loader import render_to_string

# from NewsPaper.settings import *
from news.models import PostCategory


def send_notifications(preview, pk, heading, subs):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/articles/{pk}',
        }
    )
    # решаю проблему: если несколько адресатов, в сообщеении у каждого в поле кому видны все адреса
    # перебираю список и отправляю отдельно
    # поле to д.б списком или кортежем, поэтому использую []
    for subs_ in subs:
        msg = EmailMultiAlternatives(
            subject=heading,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subs_],
        )
        # print(msg.subject, html_content)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.category.all()

        # анотация типа
        subs: list[str] = []
        for c in categories:
            subs += c.subscribers.all()

        subs = [s.email for s in subs]
        # print(subs)
        send_notifications(instance.preview(), instance.pk, instance.heading, subs)
