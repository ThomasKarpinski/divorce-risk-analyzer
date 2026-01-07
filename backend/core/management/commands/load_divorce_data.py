import csv
from django.core.management.base import BaseCommand
from core.models import DivorceData
import os

class Command(BaseCommand):
    help = 'Importing data from divorce.csv'

    def handle(self, *args, **kwargs):
        file_path = '/app/divorce.csv'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'{file_path} file not found'))
            return

        # Clear existing data to prevent duplicates
        deleted_count, _ = DivorceData.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing records.'))

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            count = 0
            for row in reader:
                DivorceData.objects.create(
                    q1=row['Atr1'], q2=row['Atr2'], q3=row['Atr3'], q4=row['Atr4'], q5=row['Atr5'],
                    q6=row['Atr6'], q7=row['Atr7'], q8=row['Atr8'], q9=row['Atr9'], q10=row['Atr10'],
                    q11=row['Atr11'], q12=row['Atr12'], q13=row['Atr13'], q14=row['Atr14'], q15=row['Atr15'],
                    q16=row['Atr16'], q17=row['Atr17'], q18=row['Atr18'], q19=row['Atr19'], q20=row['Atr20'],
                    q21=row['Atr21'], q22=row['Atr22'], q23=row['Atr23'], q24=row['Atr24'], q25=row['Atr25'],
                    q26=row['Atr26'], q27=row['Atr27'], q28=row['Atr28'], q29=row['Atr29'], q30=row['Atr30'],
                    q31=row['Atr31'], q32=row['Atr32'], q33=row['Atr33'], q34=row['Atr34'], q35=row['Atr35'],
                    q36=row['Atr36'], q37=row['Atr37'], q38=row['Atr38'], q39=row['Atr39'], q40=row['Atr40'],
                    q41=row['Atr41'], q42=row['Atr42'], q43=row['Atr43'], q44=row['Atr44'], q45=row['Atr45'],
                    q46=row['Atr46'], q47=row['Atr47'], q48=row['Atr48'], q49=row['Atr49'], q50=row['Atr50'],
                    q51=row['Atr51'], q52=row['Atr52'], q53=row['Atr53'], q54=row['Atr54'],
                    divorce_class=row['Class']
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Sukces! Zaimportowano {count} rekordów.'))