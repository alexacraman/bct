
import os
from django.core.management.base import BaseCommand
from django.conf import settings

BASE_DIR = settings.BASE_DIR

class Command(BaseCommand):
    help = 'Amount of files in cache system'

    def handle(self, *args, **options):
        cache_dir = os.path.join(BASE_DIR, 'cache')
        if os.path.exists(cache_dir):
            files = os.listdir(cache_dir)
            cache_files_length = len(files)
            self.stdout.write(self.style.SUCCESS(f'Cache dir exists and contains {cache_files_length} files.'))
        else:
            self.stdout.write(self.style.WARNING('Cache dir does not exist'))
