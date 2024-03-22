# clearcache.py

from django.core.management.base import BaseCommand
from django .conf import settings
import shutil
import os

BASE_DIR = settings.BASE_DIR
class Command(BaseCommand):
    help = 'Clears the cache directory'

    def handle(self, *args, **options):
        cache_dir = os.path.join(BASE_DIR, 'cache') 
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            os.mkdir(cache_dir)
            self.stdout.write(self.style.SUCCESS('Cache directory cleared successfully'))
        else:
            self.stdout.write(self.style.WARNING('Cache directory does not exist'))


