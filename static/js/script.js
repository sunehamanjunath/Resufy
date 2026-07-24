// Grab references to the elements we need to control
const openModalBtn = document.getElementById('openModal');
const closeModalBtn = document.getElementById('closeModal');
const modalOverlay = document.getElementById('uploadModal');

// When "Analyze My Resume" is clicked, show the modal
openModalBtn.addEventListener('click', function() {
    modalOverlay.classList.add('active');
});

// When the "x" is clicked, hide the modal
closeModalBtn.addEventListener('click', function() {
    modalOverlay.classList.remove('active');
});

// Bonus: clicking the dark backdrop (outside the box) also closes it
modalOverlay.addEventListener('click', function(event) {
    if (event.target === modalOverlay) {
        modalOverlay.classList.remove('active');
    }
});

const openModalNavBtn = document.getElementById('openModalNav');
if (openModalNavBtn) {
    openModalNavBtn.addEventListener('click', function() {
        modalOverlay.classList.add('active');
    });
}
const uploadForm = document.getElementById('uploadForm');
const loadingMessage = document.getElementById('loadingMessage');

uploadForm.addEventListener('submit', function() {
    loadingMessage.classList.add('active');
});
