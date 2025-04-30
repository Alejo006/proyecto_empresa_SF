from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', inicio, name='inicio'),
    path('inicio_sesion/', inicio_sesion, name='inicio_sesion'),
    path('registro_usuario/', registro_usuario, name='registro_usuario'),
    path('pagina_principal/', pagina_principal, name='pagina_principal'),
    path('crear_proyecto/', crear_proyecto, name='crear_proyecto'),
    path('mensajes/', mensajes, name='mensajes'),
    path('ver_proyectos/', ver_proyectos, name='ver_proyectos'),
    path('editar_proyecto/<int:proyecto_id>/', editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:proyecto_id>/', eliminar_proyecto, name='eliminar_proyecto'),
    path('confirmarmar_eliminar/<int:proyecto_id>/', confirmar_eliminar, name='confirmar_eliminar'),
    path('crear_tarea/', crear_tarea, name='crear_tarea'),
    path('ver_tareas/', ver_tareas, name='ver_tareas'),
    path('editar_tarea/<int:tarea_id>/', editar_tarea, name='editar_tarea'),    
    path('eliminar_tarea/<int:tarea_id>/', eliminar_tarea, name='eliminar_tarea'),
    path('confirmar_eliminar_tarea/<int:tarea_id>/', confirmar_eliminar_tarea, name='confirmar_eliminar_tarea'),
    path('pagina_secundaria/', pagina_secundaria, name='pagina_secundaria'),
    path('tareas_usuario/', tareas_usuario, name='tareas_usuario'),
    path('ver_proyectos_usuario/', ver_proyectos_usuario, name='ver_proyectos_usuario'),
    path('actualizar_avance/<int:tarea_id>/', actualizar_avance, name='actualizar_avance'),

]
