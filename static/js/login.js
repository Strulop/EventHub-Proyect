

document.addEventListener('DOMContentLoaded', function(){
    var message = "Ya has sido registrado, inicia sesión para comprar tus tickets.";
    var loginModalEl = document.getElementById('loginModal');
    var loginModal = new bootstrap.Modal(loginModalEl);
    
    if(message) {
        var modalBody = loginModalEl.querySelector('.modal-body');
        var alertDiv = document.createElement('div');
        alertDiv.className = "alert alert-info";
        alertDiv.innerText = message;
        // Insertamos el mensaje antes del formulario
        modalBody.insertBefore(alertDiv, modalBody.firstChild);
    }
    
    loginModal.show();
    // Remover los parámetros de la URL para que al refrescar no se vuelva a abrir el modal
    history.replaceState(null, '', window.location.pathname);
});