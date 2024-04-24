from django.urls import path
from . import views
urlpatterns = [
    path('importar-pdf/', views.importar_pdf, name='importar_pdf'),
    path('import-success/', views.import_success, name='import_success'),
    path ('seleccionar/', views.seleccionar, name='seleccionar'),
    path ('mostrarpdf/', views.mostrarpdf, name='mostrarpdf'),
    path('materiasf/<str:codcarrera>', views.get_materiasf, name='get_materiasf')
]
