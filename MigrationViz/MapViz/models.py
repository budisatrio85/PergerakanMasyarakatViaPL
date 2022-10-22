from django.db import models
import math
import pandas as pd
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

df_pl = pd.read_csv(f"{dir_path}\\provinsi.csv")
PROV_CHOICES = list(df_pl[['province_dagri_code','province_name']].drop_duplicates().sort_values('province_dagri_code').itertuples(index=False, name=None))

class MyModel(models.Model):
  provinsi = models.CharField(max_length=6, choices=PROV_CHOICES, default='31')