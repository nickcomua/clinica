
from django.http import HttpResponse 
from clinica.serializers import *
from clinica.models import *
from rest_framework import generics
from datetime import datetime
from rest_framework import generics
from django.contrib.auth.models import User 
from rest_framework import permissions  
from rest_framework.decorators import api_view
from .permition import AppointmentPer

class LocationList(generics.ListCreateAPIView):
    # permition to edit admin only
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    # permition to edit admin only
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ServiceList(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ClientList(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class WorkerList(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class AppointementList(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        if(not Worker.objects.get(id=request.data['worker']).services.filter(id=request.data['service']).exists()):
            return HttpResponse(status=400, content="Service for this worker not available")
        try:
            s = datetime.strptime(
                request.data['start_datetime'], '%Y-%m-%dT%H:%M:%S')
        except:
            s = datetime.strptime(
                request.data['start_datetime'], '%Y-%m-%dT%H:%M')
        if(type(request.data) is QueryDict):
            print("QueryDict")
            request.data._mutable = True
        request.data['end_datetime'] = s + \
            Service.objects.get(id=request.data['service']).duration
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=str(e))

    permission_classes = [AppointmentPer, ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Appointement.objects.all()
        return Appointement.objects.filter(client__user_id=self.request.user.id) | Appointement.objects.filter(worker__user_id=self.request.user.id)
    serializer_class = AppointementSerializer


class AppointementDetail(generics.RetrieveUpdateDestroyAPIView):
    def update(self, request, *args, **kwargs):
        if(not Worker.objects.get(id=request.data['worker']).services.filter(id=request.data['service']).exists()):
            return HttpResponse(status=400, content="Service for this worker not available")
        try:
            s = datetime.strptime(
                request.data['start_datetime'], '%Y-%m-%dT%H:%M:%S')
        except:
            s = datetime.strptime(
                request.data['start_datetime'], '%Y-%m-%dT%H:%M')
        if(type(request.data) is QueryDict):
            request.data._mutable = True
        request.data['end_datetime'] = s + \
            Service.objects.get(id=request.data['service']).duration
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=str(e))

    permission_classes = [AppointmentPer, ]
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAdminUser(),)
    queryset = Appointement.objects.all()
    serializer_class = AppointementSerializer


class UserList(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def register(request):
    'username email password'
    try:
        data = request.data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        user.save()
        c = Client.objects.create(user=user)
        c.save()
        return HttpResponse(status=200, content="User created")
    except Exception as e:
        return HttpResponse(status=400, content=str(e))

# @api_view(['POST'])
# def login(request):
#     'username password'
#     try:
#         data = request.data
#         user = authenticate(username=data['username'], password=data['password'])
#         if user is not None:
#
#             return HttpResponse(status=200, content="User logged in")
#         else:
#             return HttpResponse(status=400, content="User not found")
#     except Exception as e:
#         return HttpResponse(status=400, content=str(e))
