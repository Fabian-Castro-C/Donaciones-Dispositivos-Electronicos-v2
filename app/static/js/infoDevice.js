document.addEventListener('DOMContentLoaded', () => {
    const commentsList = document.getElementById('commentsList');
    const commentForm = document.getElementById('commentForm');
    const commenterName = document.getElementById('commenterName');
    const commentText = document.getElementById('commentText');
    const imageModal = document.getElementById('imageModal');
    const closeModal = document.getElementById('closeModal');
    const images = document.querySelectorAll('.device-photo'); 

    const device_id = commentForm ? commentForm.getAttribute('data-device-id') : null;
    const loadMoreButton = document.getElementById('loadMoreButton');
    let currentPage = 2; // Empezamos desde la página 2 porque la 1 ya está cargada
    const perPage = 4; // Número de comentarios por página

    // Obtener la cantidad inicial de comentarios cargados
    const initialCommentsCount = commentsList ? commentsList.children.length : 0;

    // Mostrar u ocultar el botón basado en la cantidad inicial de comentarios
    if (loadMoreButton) {
        if (initialCommentsCount < perPage) {
            // No hay más comentarios para cargar
            loadMoreButton.style.display = 'none';
        } else {
            // Podría haber más comentarios
            loadMoreButton.style.display = 'block';
        }
    }

    // Manejar la carga de más comentarios al hacer clic en el botón
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', () => {
            fetch(`/get_comments/${device_id}/${currentPage}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const comentarios = data.comentarios;
                        comentarios.forEach(comentario => {
                            const li = document.createElement('li');
                            li.innerHTML = `
                                <strong>${comentario.nombre}</strong>
                                <span>(${new Date(comentario.fecha).toLocaleString()})</span>
                                <p>${comentario.texto}</p>
                            `;
                            commentsList.appendChild(li);
                        });

                        currentPage++; // Incrementar la página para futuras solicitudes

                        if (comentarios.length < perPage) {
                            // No hay más comentarios para cargar
                            loadMoreButton.style.display = 'none';
                        }
                    } else {
                        console.error("Error al cargar más comentarios:", data.message);
                        loadMoreButton.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error("Error al enviar la solicitud:", error);
                    loadMoreButton.style.display = 'none';
                });
        });
    }

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
            createImageForModal(image.src.replace('_640x480.', '_1280x1024.'));
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
      if (text.length < 5 || text.length > 300) {
        showFieldMessage('commentText', 'El comentario debe tener entre 5 y 300 caracteres.', 'error');
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
        // Preparamos los datos para enviar
        const newComment = {
          nombre: commenterName.value.trim(),
          texto: commentText.value.trim(),
          dispositivo_id: device_id
        };

        // Realizar la solicitud al servidor
        fetch('/add_comment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newComment)
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            showFieldMessage('commentForm', 'Comentario agregado exitosamente.', 'success');
            commentForm.reset();
            // Recargar la pagina para mostrar el nuevo comentario
            setTimeout(() => {
              location.reload();
            }, 1500);
          } else if (data.errors) {
            data.errors.forEach(error => {
              showFieldMessage(error.campo, error.message, 'error');
            });
          } else {
            showFieldMessage('commentForm', 'Error al agregar el comentario. Inténtelo de nuevo.', 'error');
          }
        })
        .catch(error => {
          console.error("Error al enviar el comentario:", error);
          showFieldMessage('commentForm', 'Error al agregar el comentario. Inténtelo de nuevo.', 'error');
        })
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