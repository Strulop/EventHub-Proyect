// Variables globales
let eventoIdEliminar = null;
const eventoModalInstance = new bootstrap.Modal(document.getElementById('eventoModal'));
const eliminarModalInstance = new bootstrap.Modal(document.getElementById('eliminarModal'));

// Al abrir el modal en modo "crear"
document.querySelector('[data-bs-target="#eventoModal"]').addEventListener('click', function() {
  document.getElementById('eventoModalLabel').textContent = 'Crear Nuevo Evento';
  document.getElementById('eventoForm').reset();
  document.getElementById('eventoId').value = '';
  document.getElementById('btnSubmitEvento').textContent = 'Guardar';
  document.getElementById('eventoForm').action = '/nuevo-evento-creado';
  document.getElementById('imagenPreview').classList.add('d-none');
});

// Función para confirmar eliminación
function confirmarEliminar(id, nombre) {
  eventoIdEliminar = id;
  document.getElementById('eventoEliminarNombre').textContent = nombre;
  eliminarModalInstance.show();
}

// Enviar formulario oculto para eliminar
document.getElementById('confirmarEliminar').addEventListener('click', function() {
  if (eventoIdEliminar) {
    const form = document.getElementById('deleteForm');
    form.action = '/eliminar-evento/' + eventoIdEliminar;
    form.submit();
  }
});

// Función para editar un evento; se recibe el objeto completo gracias a tojson
function editarEvento(evento) {
  document.getElementById('eventoModalLabel').textContent = 'Editar Evento';
  document.getElementById('eventoId').value = evento.id;
  document.getElementById('nombre').value = evento.nombre;
  document.getElementById('precio').value = evento.precio;
  document.getElementById('descripcion').value = evento.descripcion;
  let fechaISO = new Date(evento.fecha).toISOString().split('T')[0];
  document.getElementById('fecha').value = fechaISO;
  document.getElementById('hora_inicio').value = evento.hora_inicio;
  document.getElementById('duracion').value = evento.duracion;
  document.getElementById('capacidad').value = evento.capacidad;
  document.getElementById('tickets_disponibles').value = evento.tickets_disponibles;
  document.getElementById('id_categoria').value = evento.id_categoria;
  document.getElementById('id_ubicacion').value = evento.id_ubicacion;
  document.getElementById('url_imagen').value = evento.url_imagen;
  
  // Mostrar vista previa de la imagen
  const imagenPreview = document.getElementById('imagenPreview');
  imagenPreview.src = evento.url_imagen;
  imagenPreview.classList.remove('d-none');

  document.getElementById('btnSubmitEvento').textContent = 'Editar';
  document.getElementById('eventoForm').action = '/editar-evento';
  eventoModalInstance.show();
}

// Vista previa de la imagen al escribir la URL
document.getElementById('url_imagen').addEventListener('input', function() {
  const url = this.value;
  const imagenPreview = document.getElementById('imagenPreview');
  if (url) {
    imagenPreview.src = url;
    imagenPreview.classList.remove('d-none');
    imagenPreview.onerror = function() {
      imagenPreview.classList.add('d-none');
      alert('La URL de la imagen no es válida');
    };
  } else {
    imagenPreview.classList.add('d-none');
  }
});

// Validación de tickets disponibles no mayor que capacidad
document.getElementById('tickets_disponibles').addEventListener('input', function() {
  const capacidad = parseInt(document.getElementById('capacidad').value) || 0;
  const disponibles = parseInt(this.value) || 0;
  if (disponibles > capacidad) {
    alert('Los tickets disponibles no pueden ser mayores que la capacidad total');
    this.value = capacidad;
  }
});

// Filtrado de eventos (lógica a implementar según necesidad)
document.getElementById('filterButton').addEventListener('click', function() {
  const categoria = document.getElementById('categoriaFilter').value;
  const ubicacion = document.getElementById('ubicacionFilter').value;
  const busqueda = document.getElementById('searchInput').value.toLowerCase();
  console.log('Filtrando eventos:', { categoria, ubicacion, busqueda });
});