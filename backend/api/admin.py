from django.contrib import admin
from .models import Universidad, Profesor, Facultad, Opinion

admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Profesor)
admin.site.register(Opinion)