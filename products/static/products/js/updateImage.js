document.addEventListener('DOMContentLoaded', function() {
  const imageInput = document.getElementById('image-input');
  const selectedImagesContainer = document.getElementById('selected-images');
  const imageUploadForm = document.getElementById('image-upload-form');

  let selectedFiles = [];

  imageInput.addEventListener('change', function() {
    for (let i = 0; i < this.files.length; i++) {
      selectedFiles.push(this.files[i]);
    }
    renderSelectedImages();
  });

  function renderSelectedImages() {
    selectedImagesContainer.innerHTML = '';

    selectedFiles.forEach((file, index) => {
      const reader = new FileReader();

      reader.onload = function(e) {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-4';

        const imageWrapper = document.createElement('div');
        imageWrapper.className = 'mb-3 text-center position-relative';

        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'img-fluid mb-2';
        img.alt = 'Preview slike';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-danger btn-sm position-absolute top-0 end-0';
        removeBtn.innerHTML = '&times;';
        removeBtn.style.zIndex = '10';

        removeBtn.addEventListener('click', () => {
          selectedFiles.splice(index, 1);
          renderSelectedImages();
          updateFileInput();
        });

        imageWrapper.appendChild(img);
        imageWrapper.appendChild(removeBtn);
        colDiv.appendChild(imageWrapper);
        selectedImagesContainer.appendChild(colDiv);
      };

      reader.readAsDataURL(file);
    });
  }

  function updateFileInput() {
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    imageInput.files = dataTransfer.files;
  }

  imageUploadForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const productId = this.dataset.productId;
    const url = `/products/${productId}/upload-images/`;

    const formData = new FormData();
    selectedFiles.forEach(file => formData.append('images', file));

    const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    })
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      // Samo refresha stranicu, ne dira DOM slike
      location.reload();
    })
    .catch(error => {
      console.error('Greška pri uploadu:', error);
      alert('Greška pri dodavanju slika.');
    });
  });
});
