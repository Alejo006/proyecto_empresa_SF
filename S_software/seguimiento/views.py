from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views hdeere.
def inicio(request):
    return render(request, 'inicio.html')

def mensajes(request):
    return render(request, 'mensajes.html')  # Usamos el template de mensajes

def confirmar_eliminar(request):
    return render(request, 'confirmar_eliminar.html')  # Usamos el template de confirmar_eliminar

def confirmar_eliminar_tarea(request):
    return render(request, 'confirmar_eliminar_tarea.html') 


def inicio_sesion(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        contrasena = request.POST.get('password')

        # Primero verificar si es un administrador
        try:
            administrador = Administrador.objects.get(correo=correo)
            if administrador.contrasena == contrasena:
                request.session['administrador_id'] = administrador.id
                messages.success(request, "Bienvenido, administrador.")
                return redirect('pagina_principal')  # Página del administrador
            else:
                messages.error(request, 'Contraseña incorrecta para administrador.')
                return redirect('inicio_sesion')

        except Administrador.DoesNotExist:
            pass  # Si no es admin, seguimos con Usuario

        # Luego verificar si es un usuario normal
        try:
            usuario = Usuario.objects.get(correo=correo)
            if usuario.contrasena == contrasena:
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombreCompleto
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('pagina_secundaria')  # Página del usuario normal
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo no registrado.')

        return redirect('inicio_sesion')

    return render(request, 'inicio_sesion.html')


def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('usuario')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        documento = request.POST.get('Documento')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('registro_usuario')

        usuario = Usuario(
            nombreCompleto=nombre,
            correo=correo,
            telefono=telefono,
            ano_nacimiento=fecha_nacimiento if fecha_nacimiento else None,
            direccion=direccion,
            documento=documento,
            contrasena=contrasena, 
            rol=rol
            # Luego podemos mejorar esto cifrando
        )
        usuario.save()

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('inicio_sesion')

    return render(request, 'registro_usuario.html')


def pagina_principal(request):
    if 'administrador_id' not in request.session:
        return redirect('inicio_sesion')

    administrador = Administrador.objects.get(id=request.session['administrador_id'])
    proyectos = Proyecto.objects.all()

    context = {
        'administrador': administrador,
        'proyectos': proyectos,
    }
    return render(request, 'pagina_principal.html', context)

def pagina_secundaria(request):
    if 'usuario_id' not in request.session:
        return redirect('inicio_sesion')

    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    proyectos = Proyecto.objects.all()

    context = {
        'usuario': usuario,
        'proyectos': proyectos,
    }
    return render(request, 'pagina_secundaria.html', context)



#@login_required  # Asegúrate de que el acceso esté restringido a usuarios logueados si es necesario


def crear_proyecto(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Crear el proyecto
        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # Agregar un mensaje de éxito
        messages.success(request, 'Proyecto creado con éxito.')

        # Redirigir a la página de mensajes
        return redirect('mensajes')

    return render(request, 'crear_proyecto.html')



def ver_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'ver_proyectos.html', {'proyectos': proyectos})

def ver_proyectos_usuario(request):
    proyectos = Proyecto.objects.all()  # muestra todo, pero sin editar/eliminar
    return render(request, 'ver_proyectos_usuario.html', {'proyectos': proyectos})


def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        proyecto.nombre = request.POST.get('nombre')
        proyecto.descripcion = request.POST.get('descripcion')
        proyecto.fecha_inicio = request.POST.get('fecha_inicio')
        proyecto.fecha_fin = request.POST.get('fecha_fin')
        proyecto.save()

        messages.success(request, 'Proyecto actualizado con éxito.')
        return redirect('ver_proyectos')

    return render(request, 'editar_proyecto.html', {'proyecto': proyecto})



def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado con éxito.')
        return redirect('ver_proyectos')

    return render(request, 'confirmar_eliminar.html', {'proyecto': proyecto})





def crear_tarea(request):
    proyectos = Proyecto.objects.all()
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        proyecto_id = request.POST.get('proyecto')
        usuario_id = request.POST.get('usuario_asignado')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estado = request.POST.get('estado')

        proyecto = Proyecto.objects.get(id=proyecto_id)
        usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

        Tarea.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            proyecto=proyecto,
            usuario_asignado=usuario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado
        )

        messages.success(request, 'Tarea creada exitosamente.')
        return redirect('mensajes')  # o donde prefieras redirigir

    return render(request, 'crear_tarea.html', {
        'proyectos': proyectos,
        'usuarios': usuarios,
    })



def ver_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'ver_tareas.html', {'tareas': tareas})


def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    proyectos = Proyecto.objects.all()
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        tarea.nombre = request.POST.get('nombre')
        tarea.descripcion = request.POST.get('descripcion')
        tarea.proyecto_id = request.POST.get('proyecto')
        tarea.usuario_asignado_id = request.POST.get('usuario_asignado') or None
        tarea.fecha_inicio = request.POST.get('fecha_inicio')
        tarea.fecha_fin = request.POST.get('fecha_fin')
        tarea.estado = request.POST.get('estado')
        tarea.save()

        messages.success(request, 'Tarea actualizada con éxito.')
        return redirect('ver_tareas')

    return render(request, 'editar_tarea.html', {
        'tarea': tarea,
        'proyectos': proyectos,
        'usuarios': usuarios
    })


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada con éxito.')
        return redirect('ver_tareas')

    return render(request, 'confirmar_eliminar_tarea.html', {'tarea': tarea})







def tareas_usuario(request):
    if 'usuario_id' not in request.session:
        return redirect('inicio_sesion')

    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    tareas = Tarea.objects.filter(usuario_asignado=usuario)  # Solo tareas asignadas a este usuario

    context = {
        'usuario': usuario,
        'tareas': tareas,
    }
    return render(request, 'tareas_usuario.html', context)


def actualizar_avance(request, tarea_id):
    if 'usuario_id' not in request.session:
        return redirect('inicio_sesion')

    tarea = Tarea.objects.get(id=tarea_id)

    if request.method == 'POST':
        nuevo_avance = request.POST.get('avance')
        tarea.avance = nuevo_avance
        tarea.save()
        messages.success(request, 'Avance actualizado correctamente.')
        return redirect('tareas_usuario')

    context = {
        'tarea': tarea,
    }
    return render(request, 'actualizar_avance.html', context)