from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversidadList, UniversidadDetailViews, FacultadList, ProfesorList, OpinionViewSet, ProfesorDetail, ProfesorViewSet, VerifyEmailView

router = DefaultRouter()
router.register(
    r'universidades/(?P<universidad_id>\d+)/facultades/(?P<facultad_id>\d+)/profesores',
    ProfesorViewSet,
    basename='profesor'
)
router.register(
    r'universidades/(?P<universidad_id>\d+)/facultades/(?P<facultad_id>\d+)/profesores/(?P<profesor_id>\d+)/opiniones',
    OpinionViewSet,
    basename='opinion'
)
urlpatterns = [
    path("universidades/", UniversidadList.as_view(), name="universidad-list"),
    path("universidades/<int:pk>/", UniversidadDetailViews.as_view(), name="universidad-detail"),
    path("universidades/<int:pk>/facultades/", FacultadList.as_view(), name="universidad-facultad-list"),
    path("", include(router.urls)),
    path("universidades/<int:universidadId>/facultades/<int:facultadId>/profesores/<int:pk>/", ProfesorDetail.as_view(), name="profesor-detail"),
    path("", include(router.urls)),
    path('auth/verify-email/', VerifyEmailView.as_view())
]