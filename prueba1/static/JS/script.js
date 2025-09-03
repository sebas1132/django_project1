function mostrarFormulario(tipo) {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (tipo === 'login') {
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
  } else if (tipo === 'register') {
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
  }
}