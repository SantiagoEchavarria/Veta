
const slides = [
    document.getElementById('slide1'),
    document.getElementById('slide2'),
    document.getElementById('slide3')
];
let currentIndex = 0;
let interval;

function showSlide(index) {
    slides.forEach(slide => slide.classList.add('hidden'));
    slides[index].classList.remove('hidden');
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
}

function startRotation() {
    interval = setInterval(nextSlide, 3000);
}

function stopRotation() {
    clearInterval(interval);
}

document.getElementById('hero').addEventListener('mouseenter', stopRotation);
document.getElementById('hero').addEventListener('mouseleave', startRotation);

startRotation();