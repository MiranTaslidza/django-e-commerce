
// Onemogući automatsko traženje svih formi sa klasom .dropzone
Dropzone.autoDiscover = false;

// Učitaj CSRF token iz šablona
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Inicijaliziraj Dropzone na tvojoj formi
const myDropzone = new Dropzone("#my-awesome-dropzone", {
    url: "/file-upload/",      // mora poklapati sa action u formi i urls.py
    paramName: "file",         // ključ pod kojim Django očekuje fajl
    maxFilesize: 5,            // maksimalna veličina u MB
    acceptedFiles: 'image/*',  // dozvoljene samo slike
    //addRemoveLinks: true, //brisanje sliika     // dodaj link za brisanje fajla
    headers: {
        "X-CSRFToken": csrftoken
    },
    init: function () {
        this.on("sending", function(file, xhr, formData) {
            // ovdje možeš dodati dodatne polja u formData, npr. korisnički ID
            // formData.append("user_id", someUserId);
        });
        this.on("success", function (file, response) {
            console.log("Upload uspješan:", response);
            // npr. prikaži thumbnail ili sačuvaj response.image_url
        });
        this.on("error", function (file, errorMessage) {
            console.error("Greška pri uploadu:", errorMessage);
        });
}
});

