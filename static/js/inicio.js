document.addEventListener('DOMContentLoaded', function() {
    const loginOption = document.getElementById('loginOption');
    const registerOption = document.getElementById('registerOption');
    const slider = document.getElementById('slider');
    const actionBtn = document.getElementById('actionBtn');
    
    // Estado inicial
    let isLogin = true;
    
    // Función para actualizar el estado
    function updateState() {
        if (isLogin) {
            slider.classList.remove('right');
            loginOption.classList.add('active');
            registerOption.classList.remove('active');
            actionBtn.textContent = 'Iniciar Sesión';
        } else {
            slider.classList.add('right');
            loginOption.classList.remove('active');
            registerOption.classList.add('active');
            actionBtn.textContent = 'Crear Cuenta';
        }
    }
    
    // Event listeners
    loginOption.addEventListener('click', function() {
        if (!isLogin) {
            isLogin = true;
            updateState();
        }
    });
    
    registerOption.addEventListener('click', function() {
        if (isLogin) {
            isLogin = false;
            updateState();
        }
    });
    
    actionBtn.addEventListener('click', function() {
        if (isLogin) {
            window.location.href = "{% url 'iniciar_seccion' %}";
        } else {
            window.location.href = "{% url 'crear_seccion' %}";
        }
    });
    
    // Inicializar
    updateState();
});