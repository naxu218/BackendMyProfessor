from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import Universidad, Facultad, Profesor, Opinion
from .serializers import CustomTokenObtainPairSerializer, OpinionSerializer, UniversidadListSerializer, UniversidadDetailSerializer,FacultadSerializer, ProfesorSerializer, UsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

class HomeView(generics.CreateAPIView):
    permission_classes = [AllowAny]

class UniversidadList(generics.ListAPIView):
    queryset = Universidad.objects.all()
    serializer_class = UniversidadListSerializer
    permission_classes = [AllowAny]

class UniversidadDetailViews(generics.RetrieveAPIView):
    queryset = Universidad.objects.all()
    serializer_class = UniversidadDetailSerializer
    permission_classes = [AllowAny]

class FacultadList(generics.ListAPIView):
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        universidad_id = self.kwargs.get('pk')
        return Facultad.objects.filter(universidad_id=universidad_id)

class ProfesorList(generics.ListAPIView):
    serializer_class = ProfesorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        universidad_id = self.kwargs['universidadId']
        facultad_id = self.kwargs['facultadId']
        return Profesor.objects.filter(facultad_id=facultad_id, facultad__universidad_id=universidad_id)

class ProfesorDetail(generics.RetrieveAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [AllowAny]

class OpinionViewSet(viewsets.ModelViewSet):
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        profesor_id = self.kwargs['profesor_id']
        return Opinion.objects.filter(profesor_id=profesor_id)
    
    def create(self, request, universidad_id=None, facultad_id=None, profesor_id=None):
        user = request.user
        profesor = get_object_or_404(Profesor, id=profesor_id, facultad_id=facultad_id, facultad__universidad_id=universidad_id,)
        if user.universidad.id != int(universidad_id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profesor=profesor, usuario=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ProfesorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfesorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        universidad_id = self.kwargs["universidad_id"]
        facultad_id = self.kwargs["facultad_id"]

        return Profesor.objects.filter(
            facultad_id = facultad_id,
            facultad_id__universidad_id = universidad_id
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        universidad_id = self.kwargs.get("universidad_id")
        facultad_id = self.kwargs.get("facultad_id")

        facultad = get_object_or_404(Facultad, id=facultad_id, universidad_id=universidad_id)
        if user.universidad.id != int(universidad_id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(facultad=facultad)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer