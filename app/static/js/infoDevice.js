document.addEventListener('DOMContentLoaded', () => {
    const commentsList = document.getElementById('commentsList');
    const commentForm = document.getElementById('commentForm');
    const commenterName = document.getElementById('commenterName');
    const commentText = document.getElementById('commentText');
    const imageModal = document.getElementById('imageModal');
    const closeModal = document.getElementById('closeModal');
    const images = document.querySelectorAll('.device-photo'); 
  
    // Crear y añadir la imagen al modal
    function createImageForModal(imageSrc) {
      const img = document.createElement('img');
      img.className = 'modal-content';
      img.id = 'expandedImage';
      img.alt = 'Imagen expandida';
      img.src = imageSrc; // Establecer el src dinámicamente
    
      // Obtener el contenedor de la imagen en el modal
      const modalImageContainer = document.getElementById('modalImageContainer');
    
      // Limpiar el contenido actual del contenedor de la imagen
      modalImageContainer.innerHTML = '';
    
      // Añadir la imagen al contenedor
      modalImageContainer.appendChild(img);
    
      // Mostrar el modal añadiendo la clase 'show'
      imageModal.classList.add('show');

      // Detener propagación en la imagen
      img.addEventListener('click', (event) => {
        event.stopPropagation();
      });
    }

    // Añadir evento de clic a cada imagen
    images.forEach(image => {
        image.addEventListener('click', () => {
            createImageForModal(image.src.replace('640x480_.', '1280x1024_.'));
            imageModal.style.display = 'flex';
        });
    });   
  
    // Mostrar mensajes para campos específicos
    function showFieldMessage(fieldId, message, type) {
      let fieldMessage = document.querySelector(`#${fieldId}Message`);
      if (!fieldMessage) {
        fieldMessage = document.createElement('div');
        fieldMessage.id = `${fieldId}Message`;
        document.querySelector(`#${fieldId}`).insertAdjacentElement('afterend', fieldMessage);
      }
      fieldMessage.innerHTML = `<p style="color: ${type === 'error' ? 'red' : 'green'};">${message}</p>`;
    }
  
    // Limpiar mensajes para todos los campos
    function clearAllMessages() {
      const allMessages = document.querySelectorAll('div[id$="Message"]');
      allMessages.forEach(message => message.innerHTML = '');
    }
  
    // Validar y manejar el formulario de comentarios
    function validateCommentForm() {
      let isValid = true;
      clearAllMessages(); // Limpiar mensajes anteriores
  
      // Validar nombre del comentarista
      const name = commenterName.value.trim();
      if (name.length < 3 || name.length > 80) {
        showFieldMessage('commenterName', 'El nombre debe tener entre 3 y 80 caracteres.', 'error');
        isValid = false;
      }
  
      // Validar texto del comentario
      const text = commentText.value.trim();
      if (text.length < 5) {
        showFieldMessage('commentText', 'El comentario debe tener al menos 5 caracteres.', 'error');
        isValid = false;
      }
  
      return isValid;
    }
  
    // Añadir comentario a la lista
    function addCommentToList(comment) {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${comment.nombre} (${comment.fecha}):</strong> ${comment.contenido}`;
      commentsList.appendChild(li);
    }
  
    // Manejar el envío del formulario de comentarios
    commentForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (validateCommentForm()) {
        const newComment = {
          nombre: commenterName.value.trim(),
          fecha: new Date().toLocaleDateString(), // Fecha actual
          contenido: commentText.value.trim()
        };
        addCommentToList(newComment);
        showFieldMessage('commentForm', 'Comentario agregado exitosamente.', 'success');
        commentForm.reset(); // Limpiar el formulario
      }
    });
  
    // Manejar el cierre del modal
    closeModal.addEventListener('click', () => {
      imageModal.style.display = 'none';
    });
  
    // Cerrar el modal si el usuario hace clic fuera del contenido del modal
    window.addEventListener('click', (event) => {
      if (event.target === imageModal) {
        imageModal.style.display = 'none';
      }
    });
  });