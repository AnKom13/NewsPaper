from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


# ТЗ: Напишите команду для manage.py, которая будет удалять все новости из какой-либо категории,
# но только при подтверждении действия в консоли при выполнении команды.


class Command(BaseCommand):
    help = 'Удаляет НОВОСТИ из указанных категорий'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('arg', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        answer = input(f'Вы правда хотите удалить все статьи в категориях {options["arg"]}? yes/no  ->')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Ну нет, так нет.'))
            return
        try:
            cat = Category.objects.filter(name__in=options['arg'])
            Post.objects.filter(category__in=cat).filter(property__exact='N').delete()
            # вывод в консоли зеленым цветом
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from categories {options["arg"]}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Что-то пошло не так.'))
