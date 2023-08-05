from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

from csgoogleanalytics.utils import create_page_stats
from csgoogleanalytics.models import Page, PageStats, PERIOD_CHOICES_FULL

from django.core.paginator import Paginator
from time import sleep

"""
class Command(BaseCommand):
    help = 'Ze egunetako datuak ekarri nahi dituzu, pageviews'

    def add_arguments(self, parser):
        default_eguna = int(datetime.now().strftime('%Y%m%d'))
        parser.add_argument('--eguna', type=int, nargs='?', default=default_eguna)

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(kwargs['eguna']))
        end_date = datetime.strptime(str(kwargs['eguna']),'%Y%m%d').date()
        end_date_str = end_date.strftime('%Y-%m-%d')

        for period_id, period_value in PERIOD_CHOICES_FULL.items():
            start_date = end_date - period_value[1]
            start_date_int = int(start_date.strftime('%Y%m%d'))
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            pages = Page.objects.filter(added_day=start_date_int)            

            if pages.exists():
                pagepaths = list(pages.values_list('pagepath',flat=True))
                boo = create_page_stats(pagepaths,start_date_str, end_date_str, period_id)

            self.stdout.write(self.style.SUCCESS('{} - {}: {}'.format(start_date,end_date, pages.count())))                                            
"""


def pasa_bertsoaldiak(bertsoaldiak):
    for b in bertsoaldiak:
        p = Page()
        p.pagepath = b.get_absolute_url()
        p.added_at = b.created_date.date()
        p.content_type = ContentType.objects.get_for_model(b).pk
        p.object_id = b.pk
        p.save()
    return True

def ekarri_egun_hontakoak(eguna):
    end_date = eguna
    end_date_str = end_date.strftime('%Y-%m-%d')

    for period_id, period_value in PERIOD_CHOICES_FULL.items():
        start_date = end_date - period_value[1]
        start_date_int = int(start_date.strftime('%Y%m%d'))
        start_date_str = start_date.strftime('%Y-%m-%d')
        
        pages = Page.objects.filter(added_day=start_date_int)            

        if pages.exists():
            pagepaths = list(pages.values_list('pagepath',flat=True))
            boo = create_page_stats(pagepaths,start_date_str, end_date_str, period_id)
    return True

class Command(BaseCommand):
    help = 'Ekarri egun bateko pageviews-ak (edo egun batzutakoak)'

    def add_arguments(self, parser):
        default_eguna = int(datetime.now().strftime('%Y%m%d'))
        parser.add_argument('--hasi', type=int, nargs='?', default=default_eguna)
        parser.add_argument('--bukatu', type=int, nargs='?', default=0)

    def handle(self, *args, **kwargs):
        try:
            hasi = datetime.strptime(str(kwargs['hasi']),'%Y%m%d').date()
            if kwargs['bukatu']:
                bukatu = datetime.strptime(str(kwargs['bukatu']),'%Y%m%d').date()
            else:
                bukatu = hasi
        except  Exception,e:
            raise CommandError('EZ da data formatu egokia. Adib.: 20151231. {}'.format(e))

        bukatu += timedelta(days=1)

        for i in range(0, (bukatu-hasi).days):
            eguna = hasi + timedelta(days=i)
            boo = ekarri_egun_hontakoak(eguna)
            sleep(2)
            self.stdout.write(self.style.SUCCESS('{}'.format(eguna,)))

