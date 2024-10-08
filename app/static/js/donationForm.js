document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('donationForm');
  const deviceContainer = document.getElementById('deviceContainer');
  const addDeviceButton = document.getElementById('addDevice');
  const regionSelect = document.getElementById('region');
  const comunaSelect = document.getElementById('comuna');
  const confirmationSection = document.getElementById('confirmationSection');
  const confirmButton = document.getElementById('confirmButton');
  const cancelButton = document.getElementById('cancelButton');
  let deviceEntryCounter = 1;

  // Actualizar comunas según la región
  regionSelect.addEventListener('change', (event) => {
    const regionId = event.target.value;

    if (regionId) {
      comunaSelect.disabled = false;
      fetch(`/get_comunas/${regionId}`)
        .then(response => response.json())
        .then(data => {
          if (data.comunas) {
            comunaSelect.innerHTML = '<option value="">Seleccione su comuna</option>';
            data.comunas.forEach(comuna => {
              const option = document.createElement('option');
              option.value = comuna.id;
              option.textContent = comuna.nombre;
              comunaSelect.appendChild(option);
            });
          } else {
            comunaSelect.innerHTML = '<option value="">No se encontraron comunas</option>';
          }
        })
        .catch(error => {
          console.error('Error al cargar comunas:', error);
          comunaSelect.innerHTML = '<option value="">Error al cargar comunas</option>';
        });
    } else {
      comunaSelect.disabled = true;
      comunaSelect.innerHTML = '<option value="">Seleccione su comuna</option>';
    }
  });

  function addDeviceEntry() {
    const originalDeviceEntry = document.getElementById('device-entry');
    const newDeviceEntry = originalDeviceEntry.cloneNode(true);

    newDeviceEntry.removeAttribute('id');
    newDeviceEntry.classList.add('device-entry');

    const inputs = newDeviceEntry.querySelectorAll('input, select');
    inputs.forEach(input => {
      input.value = '';
      if (input.type === 'file') {
        input.value = null; // reset file input
      }

      // Remove any field messages
      let fieldMessage = input.nextElementSibling;
      if (fieldMessage && fieldMessage.classList.contains('field-message')) {
        fieldMessage.parentNode.removeChild(fieldMessage);
      }
    });

    deviceContainer.appendChild(newDeviceEntry);
    deviceEntryCounter++;
  }

  function showFieldMessage(fieldElement, message, type) {
    let fieldMessage = fieldElement.nextElementSibling;
    if (!fieldMessage || !fieldMessage.classList.contains('field-message')) {
      fieldMessage = document.createElement('div');
      fieldMessage.classList.add('field-message');
      fieldElement.insertAdjacentElement('afterend', fieldMessage);
    }
    fieldMessage.innerHTML = `<p style="color: ${type === 'error' ? 'red' : 'green'};">${message}</p>`;
  }

  function showGlobalMessage(message, type) {
    const formMessages = document.getElementById('formMessages');
    formMessages.innerHTML = `<p style="color: ${type === 'error' ? 'red' : 'green'};">${message}</p>`;
  }

  function clearFieldMessage(fieldElement) {
    let fieldMessage = fieldElement.nextElementSibling;
    if (fieldMessage && fieldMessage.classList.contains('field-message')) {
      fieldMessage.innerHTML = '';
    }
  }

  function clearAllMessages() {
    ['nombre', 'email', 'telefono', 'region', 'comuna'].forEach(id => {
      const fieldElement = document.getElementById(id);
      if (fieldElement) clearFieldMessage(fieldElement);
    });

    const deviceEntries = Array.from(deviceContainer.getElementsByClassName('device-entry'));
    deviceEntries.forEach(entry => {
      const inputs = entry.querySelectorAll('input, select');
      inputs.forEach(input => {
        clearFieldMessage(input);
      });
    });

    const globalMessage = document.getElementById('formMessages');
    if (globalMessage) globalMessage.innerHTML = '';
  }

  function validateContactForm() {
    let isValid = true;

    const nombreInput = document.getElementById('nombre');
    const nombre = nombreInput.value.trim();
    if (nombre.length < 3 || nombre.length > 80) {
      showFieldMessage(nombreInput, 'El nombre del donante debe tener entre 3 y 80 caracteres.', 'error');
      isValid = false;
    }

    const emailInput = document.getElementById('email');
    const email = emailInput.value.trim();
    if (!/\S+@\S+\.\S+/.test(email)) {
      showFieldMessage(emailInput, 'El email del donante no es válido.', 'error');
      isValid = false;
    }

    const telefonoInput = document.getElementById('telefono');
    const telefono = telefonoInput.value.trim();
    if (telefono && (!/^\d+$/.test(telefono) || telefono.length < 10 || telefono.length > 15)) {
      showFieldMessage(telefonoInput, 'El número de celular debe contener entre 10 y 15 dígitos y solo números.', 'error');
      isValid = false;
    }

    const regionSelect = document.getElementById('region');
    const region = regionSelect.value;
    if (!region) {
      showFieldMessage(regionSelect, 'Por favor, selecciona una región.', 'error');
      isValid = false;
    }

    const comunaSelect = document.getElementById('comuna');
    const comuna = comunaSelect.value;
    if (!comuna) {
      showFieldMessage(comunaSelect, 'Por favor, selecciona una comuna.', 'error');
      isValid = false;
    }

    return isValid;
  }

  function validateDeviceEntry(deviceEntry) {
    let isValid = true;

    const nombreDispositivoInput = deviceEntry.querySelector('input[name="nombreDispositivo"]');
    const nombreDispositivo = nombreDispositivoInput.value.trim();
    if (nombreDispositivo.length < 3 || nombreDispositivo.length > 100) {
      showFieldMessage(nombreDispositivoInput, 'El nombre del dispositivo debe tener entre 3 y 100 caracteres.', 'error');
      isValid = false;
    }

    const tipoSelect = deviceEntry.querySelector('select[name="tipo"]');
    const tipo = tipoSelect.value;
    if (!tipo) {
      showFieldMessage(tipoSelect, 'Por favor, selecciona un tipo de dispositivo.', 'error');
      isValid = false;
    }

    const aniosUsoInput = deviceEntry.querySelector('input[name="aniosUso"]');
    const aniosUso = aniosUsoInput.value;
    if (!aniosUso || isNaN(aniosUso) || aniosUso < 0) {
      showFieldMessage(aniosUsoInput, 'Por favor, introduce un número válido de años de uso.', 'error');
      isValid = false;
    }

    const estadoSelect = deviceEntry.querySelector('select[name="estado"]');
    const estado = estadoSelect.value;
    if (!estado) {
      showFieldMessage(estadoSelect, 'Por favor, selecciona el estado del dispositivo.', 'error');
      isValid = false;
    }

    const fotosInput = deviceEntry.querySelector('input[name="fotos"]');
    const fotos = fotosInput.files;
    if (fotos.length > 3) {
      showFieldMessage(fotosInput, 'Puedes subir un máximo de 3 imágenes.', 'error');
      isValid = false;
    }

    return isValid;
  }

  function validateForm() {
    clearAllMessages();
    const isContactFormValid = validateContactForm();

    let areDevicesValid = true;
    const deviceEntries = Array.from(deviceContainer.getElementsByClassName('device-entry'));
    deviceEntries.forEach(entry => {
      const isValid = validateDeviceEntry(entry);
      if (!isValid) {
        areDevicesValid = false;
      }
    });

    return isContactFormValid && areDevicesValid;
  }

  function showConfirmationSection() {
    confirmationSection.style.display = 'block';
  }

  function hideConfirmationSection() {
    confirmationSection.style.display = 'none';
  }

  confirmButton.addEventListener('click', () => {
    showGlobalMessage('Hemos recibido la información de su donación. Muchas gracias.', 'success');
    form.reset();
    hideConfirmationSection();
    setTimeout(() => {
      window.location.href = '/';
    }, 2000);
  });

  cancelButton.addEventListener('click', () => {
    showGlobalMessage('Has cancelado la confirmación de la donación.', 'error');
    hideConfirmationSection();
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (validateForm()) {
      showConfirmationSection();
    } else {
      showGlobalMessage('Por favor, corrige los errores en el formulario.', 'error');
    }
  });

  addDeviceButton.addEventListener('click', () => {
    addDeviceEntry();
  });
});
