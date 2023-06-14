from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.db.models import Sum
import pandas as pd

import json

class AnalisisProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        # cash flow
        cash_flow = Cost_Project.objects.all().values()
        df_cash = pd.DataFrame(cash_flow)

        df_cash['total_keseluruhan'] = df_cash[['cost_design', 'cost_operasional', 'cost_produksi', 'cost_bahan', 'cost_lain']].sum(axis=1, numeric_only=True)

        df_cash['created_at'] = pd.to_datetime(df_cash['created_at'])

        df_cash_total = df_cash.groupby(df_cash['created_at'].dt.strftime('%B'))['cost_design', 'cost_operasional', 'cost_produksi', 'cost_bahan', 'cost_lain', 'total_keseluruhan'].sum().sort_values(by='created_at')

        print("df_cash_total", df_cash_total)
        
        # project statistic
        project = Project.objects.all().values()
        df_project = pd.DataFrame(project)

        # df_projects = df_project[df_project['status'].str.contains("On Progress", case=False)]
        # df_project_done = df_project[df_project['status'].str.contains("Projek Selesai", case=False)]
        df_project['created_at'] = pd.to_datetime(df_project['created_at'])
        df_project['created_at'] = df_project['created_at'].dt.strftime('%B %d, %Y, %r')
        # df_project_done['created_at'] = pd.to_datetime(df_project_done['created_at'])

        # df_d = df_project.groupby(['created_at'])['status'].apply(lambda x: x[x.str.contains('On Progress', case=False)].count()).reset_index()
        

        df_d = df_project.groupby(['created_at']).agg(
            onprogress = pd.NamedAgg(column='status', aggfunc=lambda x: x[x.str.contains('On Progress', case=False)].count()),
            done = pd.NamedAgg(column='status', aggfunc=lambda x: x[x.str.contains('Projek Selesai', case=False)].count())
        )

        print("df_d", df_d.to_dict())
        # df_total_project = df_projects.groupby(df_projects['created_at'].dt.strftime('%B %d, %Y, %r'))['status'].count().sort_values()
        # df_total_project_done = df_project_done.groupby(df_project_done['created_at'].dt.strftime('%B %d, %Y, %r'))['status'].count().sort_values()

        # kategori project
        df_kategori = pd.DataFrame(project)
        redensial = df_kategori['kategori_project'].loc[df_kategori['kategori_project'] == "Residential"]
        komersial = df_kategori['kategori_project'].loc[df_kategori['kategori_project'] == "Komersial"]

        print(redensial.count()/len(df_kategori), komersial.count()/len(df_kategori))

        data = {
            'cash_flow': df_cash_total.to_dict(),
            'project': df_d.to_dict(),
            'kategori': {
                'residential': int(redensial.count()),
                'komersial' : int(komersial.count()),
            }
        }

        return response(code=200, data=data, detail_message=None)