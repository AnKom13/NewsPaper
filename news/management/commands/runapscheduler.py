import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    # print('hello from job ===============')
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    # print(last_week)
    articles = Post.objects.filter(property__exact='A').filter(time_create__gte=last_week)
    # articles = Post.objects.filter(time_create__gte=last_week)
    # print(articles)
    categories = set(articles.values_list('category__name', flat=True))
    # print(categories)
    subs = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    # print(subs)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': articles,
        }
    )
    # msg = EmailMultiAlternatives(
    #     subject='Н_о_в_ы_е статьи за неделю',
    #     body='',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=subs,
    # )
    for subs_ in subs:
        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subs_],
        )

        msg.attach_alternative(html_content, 'text/html')
        # print(html_content)
        msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            #            trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week='mon', hour='00', minute='00'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
