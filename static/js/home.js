
// Manejo del formulario de Registro
document.getElementById('registerForm').addEventListener('submit', function(e) {
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        e.preventDefault(); // Evita el envío si las contraseñas no coinciden
        return;
    }
    console.log('Registration validated');
    // Si la validación es correcta, el formulario se envía normalmente
});

// Función para filtrar eventos
document.getElementById('applyFilters').addEventListener('click', function() {
    // Obtención de los valores seleccionados en los filtros
    const categoryFilter = document.getElementById('categoryFilter').value;
    const locationFilter = document.getElementById('locationFilter').value;
    
    // Se obtienen todas las tarjetas de evento
    const eventCards = document.querySelectorAll('.event-card-container');

    eventCards.forEach(card => {
        // Leer los atributos de datos
        const eventCategory = card.dataset.category; // ya en minúsculas
        const eventLocation = card.dataset.location;   // ya en minúsculas
        
        let show = true;
        
        // Filtro por categoría
        if (categoryFilter && eventCategory !== categoryFilter) {
            show = false;
        }
        
        // Filtro por ubicación
        if (locationFilter && eventLocation !== locationFilter) {
            show = false;
        }
        
        // Mostrar u ocultar la tarjeta según el filtrado
        card.style.display = show ? '' : 'none';
    });
});

// Evento para cada botón "Comprar Tiket" (para usuarios invitados)
/*document.querySelectorAll('.buy-ticket').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        // Se abre el modal de invitado
        const guestModalEl = document.getElementById('guestModal');
        const guestModal = new bootstrap.Modal(guestModalEl);
        guestModal.show();
    });
});*/

// Botón "Iniciar Sesión" dentro del modal de invitado
document.getElementById('guestLoginBtn').addEventListener('click', function() {
    // Cerrar modal de invitado
    const guestModalEl = document.getElementById('guestModal');
    const guestModal = bootstrap.Modal.getInstance(guestModalEl);
    guestModal.hide();
    
    // Abrir modal de login
    const loginModalEl = document.getElementById('loginModal');
    const loginModal = new bootstrap.Modal(loginModalEl);
    loginModal.show();
});

// Botón "Registrarse" dentro del modal de invitado
document.getElementById('guestRegisterBtn').addEventListener('click', function() {
    // Cerrar modal de invitado
    const guestModalEl = document.getElementById('guestModal');
    const guestModal = bootstrap.Modal.getInstance(guestModalEl);
    guestModal.hide();
    
    // Abrir modal de registro
    const registerModalEl = document.getElementById('registerModal');
    const registerModal = new bootstrap.Modal(registerModalEl);
    registerModal.show();
});



document.querySelectorAll('.buy-ticket').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log("Llego: "+ isLoggedIn)
        // Si el usuario NO está logueado, redirige a la ruta de compra
        if (isLoggedIn ==false) {
            const guestModalEl = document.getElementById('guestModal');
            const guestModal = new bootstrap.Modal(guestModalEl);
            guestModal.show();
        } else {
            // Aquí podrías manejar el caso en que el usuario sí esté logueado,
            // por ejemplo, redirigir a una página de pago o abrir otro modal.
            window.location.href = '/buy-ticket/' + this.getAttribute('data-event-id');
        }
    });
});
