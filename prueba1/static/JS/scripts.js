document.getElementById('btn-iniciar').onclick = function() {
    window.location.href = "{% url 'login' %}";
};

document.getElementById('btn-registrar').onclick = function() {
    window.location.href = "{% url 'registrarse' %}";
};

document.getElementById('btn-cerrar').onclick = function() {
    window.location.href = "{% url 'inicio' %}";
};

// Validación de contraseña en tiempo real
function validatePassword() {
    const password = document.getElementById('password1');
    const reqLength = document.getElementById('req-length');
    const reqUppercase = document.getElementById('req-uppercase');
    const reqNumber = document.getElementById('req-number');
    
    if (password.value.length >= 8) {
        reqLength.classList.add('valid');
    } else {
        reqLength.classList.remove('valid');
    }
    
    if (/[A-Z]/.test(password.value)) {
        reqUppercase.classList.add('valid');
    } else {
        reqUppercase.classList.remove('valid');
    }
    
    if (/[0-9]/.test(password.value)) {
        reqNumber.classList.add('valid');
    } else {
        reqNumber.classList.remove('valid');
    }
}

// Activar validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password1');
    if (passwordInput) {
        passwordInput.addEventListener('input', validatePassword);
    }
});