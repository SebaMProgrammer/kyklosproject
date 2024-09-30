# urls.py en la carpeta de la aplicación
from django.urls import path
from .views import home, actualizar_puestos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('actualizar_puestos', actualizar_puestos, name='actualizar_puestos'),
    # Ruta para la página principal
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

