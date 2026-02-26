document.addEventListener('DOMContentLoaded', function() {
    // Buscamos el campo de tipo archivo (el de la imagen) en el formulario
    const imageInput = document.querySelector('input[type="file"]');
    // Buscamos la etiqueta de imagen donde mostraremos la vista previa
    const imagePreview = document.getElementById('image-preview');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            
            if (file) {
                // Usamos FileReader para leer el archivo seleccionado
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Le asignamos el resultado a la etiqueta <img> y la hacemos visible
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                
                reader.readAsDataURL(file);
            } else {
                // Si el usuario cancela la selección, ocultamos la imagen
                imagePreview.src = '';
                imagePreview.style.display = 'none';
            }
        });
    }
});