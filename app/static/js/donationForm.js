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
      const newId = `${input.name}-${deviceEntryCounter}`;
      input.id = newId;
      input.value = '';

      let fieldMessage = newDeviceEntry.querySelector(`#${input.name}Message`);
      if (fieldMessage) {
        fieldMessage.id = `${newId}Message`;
        fieldMessage.innerHTML = '';
      }
    });

    deviceContainer.appendChild(newDeviceEntry);
    deviceEntryCounter++;
  }

  function showFieldMessage(fieldId, message, type) {
    let fieldMessage = document.querySelector(`#${fieldId}Message`);
    if (!fieldMessage) {
      fieldMessage = document.createElement('div');
      fieldMessage.id = `${fieldId}Message`;
      document.querySelector(`#${fieldId}`).insertAdjacentElement('afterend', fieldMessage);
    }
    fieldMessage.innerHTML = `<p style="color: ${type === 'error' ? 'red' : 'green'};">${message}</p>`;
  }

  function showGlobalMessage(message, type) {
    const formMessages = document.getElementById('formMessages');
    formMessages.innerHTML = `<p style="color: ${type === 'error' ? 'red' : 'green'};">${message}</p>`;
  }

  function clearFieldMessage(fieldId) {
    const fieldMessage = document.querySelector(`#${fieldId}Message`);
    if (fieldMessage) fieldMessage.innerHTML = '';
  }

  function clearAllMessages() {
    ['nombre', 'email', 'telefono', 'region', 'comuna'].forEach(id => clearFieldMessage(id));

    const deviceEntries = Array.from(deviceContainer.getElementsByClassName('device-entry'));
    deviceEntries.forEach(entry => {
      ['nombreDispositivo', 'tipo', 'aniosUso', 'estado', 'fotos'].forEach(name => {
        const fieldMessage = entry.querySelector(`#${name}-${deviceEntryCounter - 1}Message`);
        if (fieldMessage) fieldMessage.innerHTML = '';
      });
    });

    const globalMessage = document.getElementById('formMessages');
    if (globalMessage) globalMessage.innerHTML = '';
  }

  function validateContactForm() {
    let isValid = true;

    const nombre = document.getElementById('nombre').value.trim();
    if (nombre.length < 3 || nombre.length > 80) {
      showFieldMessage('nombre', 'El nombre del donante debe tener entre 3 y 80 caracteres.', 'error');
      isValid = false;
    }

    const email = document.getElementById('email').value.trim();
    if (!/\S+@\S+\.\S+/.test(email)) {
      showFieldMessage('email', 'El email del donante no es válido.', 'error');
      isValid = false;
    }

    const telefono = document.getElementById('telefono').value.trim();
    if (telefono && (!/^\d+$/.test(telefono) || telefono.length < 10 || telefono.length > 15)) {
      showFieldMessage('telefono', 'El número de celular debe contener entre 10 y 15 dígitos y solo números.', 'error');
      isValid = false;
    }

    const region = document.getElementById('region').value;
    if (!region) {
      showFieldMessage('region', 'Por favor, selecciona una región.', 'error');
      isValid = false;
    }

    const comuna = document.getElementById('comuna').value;
    if (!comuna) {
      showFieldMessage('comuna', 'Por favor, selecciona una comuna.', 'error');
      isValid = false;
    }

    return isValid;
  }

  function validateDeviceEntry(deviceEntry) {
    let isValid = true;

    const nombreDispositivo = deviceEntry.querySelector('input[name="nombreDispositivo"]').value.trim();
    if (nombreDispositivo.length < 3 || nombreDispositivo.length > 100) {
      showFieldMessage(`${deviceEntry.querySelector('input[name="nombreDispositivo"]').id}`, 'El nombre del dispositivo debe tener entre 3 y 100 caracteres.', 'error');
      isValid = false;
    }

    const tipo = deviceEntry.querySelector('select[name="tipo"]').value;
    if (!tipo) {
      showFieldMessage(`${deviceEntry.querySelector('select[name="tipo"]').id}`, 'Por favor, selecciona un tipo de dispositivo.', 'error');
      isValid = false;
    }

    const aniosUso = deviceEntry.querySelector('input[name="aniosUso"]').value;
    if (!aniosUso || isNaN(aniosUso) || aniosUso < 0) {
      showFieldMessage(`${deviceEntry.querySelector('input[name="aniosUso"]').id}`, 'Por favor, introduce un número válido de años de uso.', 'error');
      isValid = false;
    }

    const estado = deviceEntry.querySelector('select[name="estado"]').value;
    if (!estado) {
      showFieldMessage(`${deviceEntry.querySelector('select[name="estado"]').id}`, 'Por favor, selecciona el estado del dispositivo.', 'error');
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
      window.location.href = 'index.html';
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

  loadRegions();
});
