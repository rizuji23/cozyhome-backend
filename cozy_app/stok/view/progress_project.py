from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

class ProgressProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id')
        try:
            progress = ProgressProjectSerializer(Progress_Project.objects.filter(id_project=id), many=True)

            self.data = {
                "progress_project": progress.data
            }

            return response(code=200, data=self.data, detail_message=None)

        except Progress_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data progress not found")
        
    def post(self, request):
        id_progress_project = getuuid.Ramdom_Id.get_id()
        id_project = request.data['id_project']
        nama_progress = request.data['nama_progress']
        desc = request.data['desc']
        percentage = request.data['percentage']
        status = request.data['status']
        id_user = request.data['id_user']
        
        try:
            project = Project.objects.get(id_project=id_project)

            try:
                _progress = Progress_Project(id_progress_project=id_progress_project, id_project_id=project.id, nama_progress=nama_progress, desc=desc, percentage=percentage, status=status, id_user_id=id_user)
                
                _progress.save()

                return response(code=201, data=None, detail_message="created request success")

            except Exception as e:
                return response(code=500, data=None, detail_message=str(e))
        
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
        
    def put(self, request):
        id = request.query_params.get('id')
        id_project = request.data['id_project']
        nama_progress = request.data['nama_progress']
        desc = request.data['desc']
        percentage = request.data['percentage']
        status = request.data['status']
        id_user = request.data['id_user']

        try:
            project = Project.objects.get(id_project=id_project)
            
            try:
                data = Progress_Project.objects.get(id_progress_project=id)
                try:
                    data.id_project_id = project.id
                    data.nama_progress = nama_progress
                    data.desc = desc
                    data.percentage = percentage
                    data.status = status
                    data.id_user_id = id_user

                    data.save()

                    return response(code=201, data=None, detail_message="update request success")

                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))
            except Progress_Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data progress not found")
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
    
    def delete(self, request):
        id = request.query_params.get('id')

        try:
            try:
                data = Progress_Project.objects.get(id_progress_project=id)

                data.delete()

                return response(code=201, data=None, detail_message="delete request success")

            except Progress_Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data progress not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))