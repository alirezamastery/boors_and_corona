from django.core.management.base import BaseCommand

from apps.guard.models import SecurityConfig, ViewDetail
from apps.guard.utils import list_views


class Command(BaseCommand):
    """ This command initializes the gurad
        for enhancing the security of your project.
    """
    help = 'Initialize Guard app'

    # Your code
    def handle(self, *args, **kwargs):
        view_detail_num = ViewDetail.objects.count()
        if not view_detail_num:
            for i in range(40):
                new_obj = ViewDetail.objects.create(name=str(i))
                new_obj.save()
        else:
            self.stdout('the data base is already initialized')

