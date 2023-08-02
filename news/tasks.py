from celery import shared_task
import time
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import datetime
from news.models import Post, Category


@shared_task
def send_notifications(preview, pk, heading, subs):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/articles/{pk}',
        }
    )
    for subs_ in subs:
        msg = EmailMultiAlternatives(
            subject=heading,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subs_],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    print("Zarabotalo!!!")


@shared_task
def my_job():
    #  процедура СКОПИРОВАНА из runapscheduler
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    articles = Post.objects.filter(property__exact='A').filter(time_create__gte=last_week)
    categories = set(articles.values_list('category__name', flat=True))
    subs = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': articles,
        }
    )

    for subs_ in subs:
        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subs_],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
