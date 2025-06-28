// Funkcija za dohvat CSRF tokena iz kolačića
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Aktivacija samo jednog checkboxa i AJAX za spremanje
document.querySelectorAll('.main-image-checkbox').forEach(cb => {
  cb.addEventListener('change', function () {
    if (this.checked) {
      // Isključi sve ostale checkboxe
      document.querySelectorAll('.main-image-checkbox').forEach(other => {
        if (other !== this) {
          other.checked = false;
        }
      });

      // Pošalji zahtjev serveru da postavi ovu sliku kao glavnu
      const imageId = this.value;
      fetch("/set-main-image/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: `image_id=${imageId}`
      })
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert("Greška pri postavljanju glavne slike: " + data.error);
        }
      })
      .catch(error => {
        alert("Došlo je do greške u komunikaciji sa serverom.");
        console.error(error);
      });
    }
  });
});
