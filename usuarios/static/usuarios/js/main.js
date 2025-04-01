// Efectos suaves para navegación
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.transform = 'translateY(-2px)';
        });
        link.addEventListener('mouseout', () => {
            link.style.transform = 'translateY(0)';
        });
    });
});