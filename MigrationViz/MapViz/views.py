from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView

from .forms import MyModelForm
from .models import MyModel

import pandas as pd
import os 
import math
import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))
# Create your views here.
class IndexView(CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = "index.html"

class ProsesView(View):
    model = MyModel
    form_class = MyModelForm
    template_name = "index.html"
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        provinsi = request.POST.get('provinsi','')
        # print('DONE 0')
        # df_pl = pd.read_csv(f"{dir_path}\\Peduli_Lindungi_Checkin_Hackathon.csv", sep='|')
        # df_latlong = pd.read_csv(f'{dir_path}\\list_location_id_csv.csv')
        # df_latlong['kabko_id'] = df_latlong.kabko.astype('category').cat.codes
        # df_pl['checkin_timestamp'] = pd.to_datetime(list(df_pl.checkin_timestamp.str[:-4]), format='%Y-%m-%d %H:%M:%S')
        # df_pl['kabko'] = df_pl['city_name'].str.replace('KOTA ADM. JAKARTA BARAT','KOTA JAKARTA').str.replace('KAB. ADM. KEP. SERIBU','KOTA JAKARTA').str.replace('KOTA ADM. JAKARTA PUSAT','KOTA JAKARTA').str.replace('KOTA ADM. JAKARTA TIMUR','KOTA JAKARTA').str.replace('KOTA ADM. JAKARTA UTARA','KOTA JAKARTA').str.replace('KOTA ADM. JAKARTA SELATAN','KOTA JAKARTA')
        # df_pl.kabko = df_pl.kabko.astype(str)
        # df_latlong.kabko = df_latlong.kabko.astype(str)
        # print('DONE 1')
        # df = pd.merge(df_pl, df_latlong, how='left', on='kabko')
        # all_gdf = df[['nik_hashed','checkin_timestamp','province_name','kabko','lat','long','kabko_id','province_dagri_code']].copy()
        # all_gdf['bulan'] = all_gdf.checkin_timestamp.dt.month
        # all_gdf['hari'] = all_gdf.checkin_timestamp.dt.day
        # all_gdf['jam'] = all_gdf.checkin_timestamp.dt.hour
        # all_gdf['menit'] = all_gdf.checkin_timestamp.dt.minute
        # print('DONE 2')
        # sort_df = all_gdf.sort_values(['nik_hashed','checkin_timestamp']).copy()
        # test_df = sort_df.copy()
        # test_df['next_province_name'] = None
        # test_df['next_kabko'] = None
        # test_df['next_lat'] = None
        # test_df['next_long'] = None
        # test_df['next_kabko_id'] = None
        # test_df['next_checkin_timestamp'] = None
        # test_df['next_province_dagri_code'] = None
        # print('DONE 3')
        # list_unique = []
        # for i, row in enumerate(test_df.itertuples(index=False)):
        #     if len(list_unique) < 1:
        #         list_unique.append(row)
        #     elif ((list_unique[len(list_unique)-1][0] == row.nik_hashed) &
        #             (list_unique[len(list_unique)-1][2] == row.province_name) &
        #             (list_unique[len(list_unique)-1][3] == row.kabko)):
        #             pass
        #     else:
        #         if (list_unique[len(list_unique)-1][0] == row.nik_hashed):
        #             templist = list(list_unique[len(list_unique)-1])
        #             templist[12] = row.province_name
        #             templist[13] = row.kabko
        #             templist[14] = row.lat
        #             templist[15] = row.long
        #             templist[16] = int(row.kabko_id)
        #             templist[17] = row.checkin_timestamp
        #             templist[18] = row.province_dagri_code
        #             list_unique[len(list_unique)-1] = tuple(templist)
        #         list_unique.append(row)
        # new_df = pd.DataFrame(list_unique, columns=test_df.columns)
        # print('DONE 4')
        # new_df = new_df[new_df['next_province_name'].notna()].copy()
        # new_df['kabko_id'] = new_df['kabko_id'].astype(float)
        # new_df['t'] = new_df.checkin_timestamp
        # new_df['trajectory_id'] = new_df.nik_hashed.astype('category').cat.codes
        # new_df['duration'] = new_df.next_checkin_timestamp - new_df.checkin_timestamp
        # new_df['distance_meter'] = new_df.apply(lambda x: haversine(x.long,x.lat,x.next_long,x.next_lat), axis=1)

        # proses_df = new_df[~((new_df.duration < datetime.timedelta(minutes=10))&(new_df.distance_meter > 100000))].copy()
        # print('DONE 5')
        proses_df = pd.read_csv(f'{dir_path}\\proses_data.csv')
        proses_df['province_dagri_code'] = proses_df['province_dagri_code'].astype(int)
        proses_df['next_province_dagri_code'] = proses_df['next_province_dagri_code'].astype(int)

        province_dagri_code = int(provinsi)

        from_jabodetabek_df = proses_df[(proses_df.province_dagri_code == province_dagri_code)].copy()
        from_jabodetabek_df = from_jabodetabek_df[(from_jabodetabek_df.next_province_dagri_code != province_dagri_code)].copy()
        to_jabodetabek_df = proses_df[(proses_df.next_province_dagri_code == province_dagri_code)].copy()
        to_jabodetabek_df = to_jabodetabek_df[(to_jabodetabek_df.province_dagri_code != province_dagri_code)].copy()

        move_kotadari_df = from_jabodetabek_df[['trajectory_id','kabko_id','lat','long','next_kabko_id','next_lat','next_long']]
        move_kotadari_df = move_kotadari_df.groupby(['kabko_id','lat','long','next_kabko_id','next_lat','next_long']).count()
        move_kotadari_df.reset_index(inplace=True)
        move_kotadari_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\move_kotadari.csv')

        move_kotatujuan_df = to_jabodetabek_df[['trajectory_id','kabko_id','lat','long','next_kabko_id','next_lat','next_long']]
        move_kotatujuan_df = move_kotatujuan_df.groupby(['kabko_id','lat','long','next_kabko_id','next_lat','next_long']).count()
        move_kotatujuan_df.reset_index(inplace=True)
        move_kotatujuan_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\move_kotatujuan.csv')

        kota_dari_df = from_jabodetabek_df[['kabko_id','lat','long','kabko']].drop_duplicates().reset_index(drop=True).copy()
        next_kota_dari_df = from_jabodetabek_df[['next_kabko_id','next_lat','next_long','next_kabko']].drop_duplicates().reset_index(drop=True).copy()
        next_kota_dari_df.columns = ['kabko_id','lat','long','kabko']
        frame = [kota_dari_df,next_kota_dari_df]
        kota_dari_df = pd.concat(frame).drop_duplicates().reset_index(drop=True).copy()
        kota_dari_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\kotadari.csv')

        kota_tujuan_df = to_jabodetabek_df[['kabko_id','lat','long','kabko']].drop_duplicates().reset_index(drop=True).copy()
        next_kota_tujuan_df = to_jabodetabek_df[['next_kabko_id','next_lat','next_long','next_kabko']].drop_duplicates().reset_index(drop=True).copy()
        next_kota_tujuan_df.columns = ['kabko_id','lat','long','kabko']
        frame = [kota_tujuan_df,next_kota_tujuan_df]
        kota_tujuan_df = pd.concat(frame).drop_duplicates().reset_index(drop=True).copy()
        kota_tujuan_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\kotatujuan.csv')

        top_from_df = from_jabodetabek_df[['trajectory_id','kabko','next_kabko','province_name']].groupby(['province_name','kabko','next_kabko']).count().reset_index().sort_values('trajectory_id', ascending=False)[:10].copy()
        top_from_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\top_dari.csv')

        top_to_df = to_jabodetabek_df[['trajectory_id','kabko','next_kabko','next_province_name']].groupby(['next_province_name','kabko','next_kabko']).count().reset_index().sort_values('trajectory_id', ascending=False)[:10].copy()
        top_to_df.to_csv(f'{dir_path}\\..\\..\\MigrationViz\\static\\csv\\top_tujuan.csv')
        print('DONE OK')

        return render(request, self.template_name, {'form': form})
